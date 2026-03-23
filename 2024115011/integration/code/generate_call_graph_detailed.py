"""Generate a detailed annotated function-level call graph for StreetRace Manager.

Usage:
    python streetrace_manager/generate_call_graph_detailed.py

Outputs:
    - streetrace_manager/call_graph_detailed.dot
    - streetrace_manager/call_graph_detailed.png

Annotations included:
    - Node label: module.class.method + short docstring summary
    - Cluster per module
    - Edge label: internal / cross-module
    - Edge style: solid (internal), bold blue (cross-module)
    - Legend explaining shapes/colors/styles
"""

from __future__ import annotations

import ast
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
MODULE_FILES = sorted(
    p
    for p in ROOT.glob("*.py")
    if p.name
    not in {
        "__init__.py",
        "generate_call_graph.py",
        "generate_call_graph_v2.py",
        "generate_call_graph_v3.py",
        "generate_call_graph_detailed.py",
    }
)


@dataclass
class MethodInfo:
    module: str
    class_name: str
    method_name: str
    node: ast.FunctionDef
    doc_summary: str = ""

    @property
    def symbol(self) -> str:
        return f"{self.module}.{self.class_name}.{self.method_name}"


@dataclass
class ModuleModel:
    module: str
    methods: dict[str, MethodInfo] = field(default_factory=dict)


class CallCollector(ast.NodeVisitor):
    def __init__(
        self,
        owner: MethodInfo,
        local_method_names: set[str],
        attr_class_map: dict[str, str],
    ):
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

        # self.method(...)
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == "self":
            name = func.attr
            if name in self.local_method_names:
                return f"{module}.{class_name}.{name}"

        # self.attr.method(...)
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Attribute):
            value = func.value
            if isinstance(value.value, ast.Name) and value.value.id == "self":
                attr_name = value.attr
                target_class = self.attr_class_map.get(attr_name)
                if target_class:
                    return f"{module}.{target_class}.{func.attr}"

        # direct call fn(...)
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
                    doc = ast.get_docstring(child) or ""
                    doc_summary = doc.strip().splitlines()[0] if doc else ""
                    info = MethodInfo(module_name, node.name, child.name, child, doc_summary)
                    model.methods[info.symbol] = info
    return model


def _annotation_name(annotation: ast.AST | None) -> str | None:
    if annotation is None:
        return None
    if isinstance(annotation, ast.Name):
        return annotation.id
    if isinstance(annotation, ast.Attribute):
        return annotation.attr
    if isinstance(annotation, ast.Subscript):
        return _annotation_name(annotation.value)
    return None


def build_attr_class_map(init_method: ast.FunctionDef) -> dict[str, str]:
    mapping: dict[str, str] = {}

    # parameter type map (for self.x = dependency_param)
    param_types: dict[str, str] = {}
    for arg in init_method.args.args:
        if arg.arg == "self":
            continue
        ann_name = _annotation_name(arg.annotation)
        if ann_name:
            param_types[arg.arg] = ann_name

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
            continue

        # self.x = dep_param where dep_param: SomeClass
        if isinstance(node.value, ast.Name):
            dep_type = param_types.get(node.value.id)
            if dep_type:
                mapping[target.attr] = dep_type

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

            init_symbol = f"{method.module}.{method.class_name}.__init__"
            init_method = all_methods.get(init_symbol)
            attr_map = build_attr_class_map(init_method.node) if init_method else {}

            collector = CallCollector(method, local_methods, attr_map)
            collector.visit(method.node)

            for callee in collector.calls:
                if callee in all_methods:
                    edges.add((method.symbol, callee))
                    continue

                # resolve by Class.method if module in provisional callee is local placeholder
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


def esc(text: str) -> str:
    return text.replace('"', "'")


def short_doc(summary: str, limit: int = 52) -> str:
    if not summary:
        return "(no docstring summary)"
    if len(summary) <= limit:
        return summary
    return summary[: limit - 3] + "..."


def write_dot(
    edges: set[tuple[str, str]],
    methods: dict[str, MethodInfo],
    out_path: Path,
) -> None:
    lines = [
        "digraph StreetRaceDetailedCallGraph {",
        "  rankdir=LR;",
        "  graph [fontname=Helvetica, fontsize=11, labelloc=t, labeljust=l, pad=0.2];",
        "  node  [shape=box, style=filled, fillcolor=white, color=gray40, fontname=Helvetica, fontsize=9];",
        "  edge  [fontname=Helvetica, fontsize=8, color=gray35];",
        "",
        "  label=\"StreetRace Manager – Detailed Annotated Call Graph\";",
    ]

    # Cluster by module
    by_module: dict[str, list[str]] = {}
    for symbol in methods:
        module = symbol.split(".", 1)[0]
        by_module.setdefault(module, []).append(symbol)

    module_colors = [
        "#F8FBFF",
        "#F9FFF8",
        "#FFFDF8",
        "#FFF8FC",
        "#F8FFF8",
        "#F8F8FF",
        "#FFF8F8",
        "#F8FFFE",
    ]

    for idx, (module, symbols) in enumerate(sorted(by_module.items())):
        color = module_colors[idx % len(module_colors)]
        lines.extend(
            [
                f'  subgraph "cluster_{module}" {{',
                f'    label="module: {module}";',
                '    color="#AAB4C3";',
                f'    style=filled; fillcolor="{color}";',
            ]
        )
        for sym in sorted(symbols):
            m = methods[sym]
            label = f"{sym}\\n{short_doc(m.doc_summary)}"
            lines.append(f'    "{sym}" [label="{esc(label)}"];')
        lines.append("  }")

    # Edges with annotations
    for src, dst in sorted(edges):
        src_mod = src.split(".", 1)[0]
        dst_mod = dst.split(".", 1)[0]
        cross = src_mod != dst_mod
        edge_label = "cross-module" if cross else "internal"
        if cross:
            lines.append(
                f'  "{src}" -> "{dst}" [label="{edge_label}", color="#1E6BD6", penwidth=1.6, fontcolor="#1E6BD6"];'
            )
        else:
            lines.append(
                f'  "{src}" -> "{dst}" [label="{edge_label}", color="#555555", style=solid];'
            )

    # Legend
    lines.extend(
        [
            "",
            '  subgraph "cluster_legend" {',
            '    label="Legend";',
            '    color="#C9CED6"; style=rounded;',
            '    legend_node [shape=box, label="Node: module.class.method\\n+ short docstring annotation", fillcolor="#FFFFFF"];',
            '    legend_internal_a [shape=point, width=0.01, label=""];',
            '    legend_internal_b [shape=point, width=0.01, label=""];',
            '    legend_cross_a [shape=point, width=0.01, label=""];',
            '    legend_cross_b [shape=point, width=0.01, label=""];',
            '    legend_internal_a -> legend_internal_b [label="internal", color="#555555"];',
            '    legend_cross_a -> legend_cross_b [label="cross-module", color="#1E6BD6", penwidth=1.6, fontcolor="#1E6BD6"];',
            "  }",
            "}",
        ]
    )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    models = [parse_module(path) for path in MODULE_FILES]
    methods = {symbol: m for model in models for symbol, m in model.methods.items()}
    edges = collect_edges(models)

    dot_path = ROOT / "call_graph_detailed.dot"
    png_path = ROOT / "call_graph_detailed.png"

    write_dot(edges, methods, dot_path)

    try:
        subprocess.run(["dot", "-Tpng", str(dot_path), "-o", str(png_path)], check=True)
        print(f"Generated: {dot_path}")
        print(f"Generated: {png_path}")
    except Exception:
        print(f"Generated: {dot_path}")
        print("Could not render PNG. Ensure Graphviz is installed.")


if __name__ == "__main__":
    main()
