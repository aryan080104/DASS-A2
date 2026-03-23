"""Generate a function-level call graph for StreetRace Manager modules.

Usage:
    python streetrace_manager/generate_call_graph.py

Outputs:
    - streetrace_manager/call_graph.dot
    - streetrace_manager/call_graph.mmd
    - streetrace_manager/call_graph.png (if Graphviz `dot` exists)
"""

from __future__ import annotations

import ast
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
MODULE_FILES = sorted(
    p for p in ROOT.glob("*.py") if p.name not in {"__init__.py", "generate_call_graph.py"}
)


@dataclass
class MethodInfo:
    module: str
    class_name: str
    method_name: str
    node: ast.FunctionDef

    @property
    def symbol(self) -> str:
        return f"{self.module}.{self.class_name}.{self.method_name}"


@dataclass
class ModuleModel:
    module: str
    methods: dict[str, MethodInfo] = field(default_factory=dict)


class CallCollector(ast.NodeVisitor):
    def __init__(self, owner: MethodInfo, local_method_names: set[str], attr_class_map: dict[str, str]):
        self.owner = owner
        self.local_method_names = local_method_names
        self.attr_class_map = attr_class_map
        self.calls: set[str] = set()

    def visit_Call(self, node: ast.Call) -> None:
        callee = self._resolve_call(node.func)
        if callee:
            self.calls.add(callee)
        self.generic_visit(node)

    def _resolve_call(self, func: ast.AST) -> str | None:
        module = self.owner.module
        class_name = self.owner.class_name

        # self.some_method(...)
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "self":
            name = func.attr
            if name in self.local_method_names:
                return f"{module}.{class_name}.{name}"

        # self.some_attr.some_method(...)
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Attribute):
            value = func.value
            if isinstance(value.value, ast.Name) and value.value.id == "self":
                attr_name = value.attr
                target_class = self.attr_class_map.get(attr_name)
                if target_class:
                    return f"{module}.{target_class}.{func.attr}"

        # direct function call in module: fn(...)
        if isinstance(func, ast.Name):
            return f"{module}.{func.id}"

        return None


def parse_module(path: Path) -> ModuleModel:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    module_name = path.stem
    model = ModuleModel(module_name)

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    info = MethodInfo(module_name, node.name, child.name, child)
                    model.methods[info.symbol] = info
    return model


def build_attr_class_map(init_method: ast.FunctionDef) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for node in ast.walk(init_method):
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1:
            continue

        target = node.targets[0]
        if not (
            isinstance(target, ast.Attribute)
            and isinstance(target.value, ast.Name)
            and target.value.id == "self"
        ):
            continue

        # self.x = SomeClass(...)
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            mapping[target.attr] = node.value.func.id
    return mapping


def collect_edges(models: Iterable[ModuleModel]) -> set[tuple[str, str]]:
    all_methods: dict[str, MethodInfo] = {}
    by_class_module: dict[tuple[str, str], set[str]] = {}

    for model in models:
        for symbol, method in model.methods.items():
            all_methods[symbol] = method
            key = (method.module, method.class_name)
            by_class_module.setdefault(key, set()).add(method.method_name)

    edges: set[tuple[str, str]] = set()

    for model in models:
        for method in model.methods.values():
            local_methods = by_class_module.get((method.module, method.class_name), set())

            attr_map: dict[str, str] = {}
            if method.method_name == "__init__":
                attr_map = build_attr_class_map(method.node)
            else:
                # try to find class __init__ map for methods in same class
                init_symbol = f"{method.module}.{method.class_name}.__init__"
                init_method = all_methods.get(init_symbol)
                if init_method is not None:
                    attr_map = build_attr_class_map(init_method.node)

            collector = CallCollector(method, local_methods, attr_map)
            collector.visit(method.node)

            for callee in collector.calls:
                # Keep calls that point to known methods exactly
                if callee in all_methods:
                    edges.add((method.symbol, callee))
                    continue

                # Resolve calls where module may differ but class+method are known
                if callee.count(".") >= 2:
                    _, target_class, target_method = callee.split(".", 2)
                    matches = [
                        sym
                        for sym in all_methods
                        if sym.endswith(f".{target_class}.{target_method}")
                    ]
                    if len(matches) == 1:
                        edges.add((method.symbol, matches[0]))

    return edges


def write_dot(edges: set[tuple[str, str]], methods: dict[str, MethodInfo], out_path: Path) -> None:
    lines = ["digraph StreetRaceCallGraph {", "  rankdir=LR;", "  node [shape=box, fontsize=10];"]

    # Group nodes by module for readability
    by_module: dict[str, list[str]] = {}
    for symbol in methods:
        module = symbol.split(".", 1)[0]
        by_module.setdefault(module, []).append(symbol)

    for module, symbols in sorted(by_module.items()):
        lines.append(f'  subgraph "cluster_{module}" {{')
        lines.append(f'    label="{module}";')
        lines.append("    color=lightgrey;")
        for sym in sorted(symbols):
            lines.append(f'    "{sym}";')
        lines.append("  }")

    for src, dst in sorted(edges):
        lines.append(f'  "{src}" -> "{dst}";')

    lines.append("}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_mermaid(edges: set[tuple[str, str]], out_path: Path) -> None:
    lines = ["flowchart LR"]
    for src, dst in sorted(edges):
        s = src.replace(".", "_")
        d = dst.replace(".", "_")
        lines.append(f'  {s}["{src}"] --> {d}["{dst}"]')
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    models = [parse_module(path) for path in MODULE_FILES]
    methods = {symbol: m for model in models for symbol, m in model.methods.items()}
    edges = collect_edges(models)

    dot_path = ROOT / "call_graph.dot"
    mmd_path = ROOT / "call_graph.mmd"
    png_path = ROOT / "call_graph.png"

    write_dot(edges, methods, dot_path)
    write_mermaid(edges, mmd_path)

    try:
        subprocess.run(
            ["dot", "-Tpng", str(dot_path), "-o", str(png_path)],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Generated: {dot_path}")
        print(f"Generated: {mmd_path}")
        print(f"Generated: {png_path}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Generated: {dot_path}")
        print(f"Generated: {mmd_path}")
        print("Graphviz `dot` not found (or failed). Install Graphviz to render PNG automatically.")


if __name__ == "__main__":
    main()
