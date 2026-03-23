"""Generate an alternative (cross-module focused) call graph.

Usage:
    python streetrace_manager/generate_call_graph_v2.py

Outputs:
    - streetrace_manager/call_graph_v2.dot
    - streetrace_manager/call_graph_v2.png (if Graphviz is installed)

This graph intentionally focuses on *cross-module* calls only, so you can compare
it with the full graph from generate_call_graph.py.
"""

from __future__ import annotations

import ast
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_FILES = sorted(
    p for p in ROOT.glob("*.py") if p.name not in {"__init__.py", "generate_call_graph.py", "generate_call_graph_v2.py"}
)


@dataclass(frozen=True)
class MethodRef:
    module: str
    cls: str
    method: str

    @property
    def symbol(self) -> str:
        return f"{self.module}.{self.cls}.{self.method}"


def parse_methods(path: Path) -> tuple[dict[str, MethodRef], dict[tuple[str, str], ast.FunctionDef]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    module = path.stem
    methods: dict[str, MethodRef] = {}
    ast_map: dict[tuple[str, str], ast.FunctionDef] = {}

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    ref = MethodRef(module, node.name, child.name)
                    methods[ref.symbol] = ref
                    ast_map[(node.name, child.name)] = child
    return methods, ast_map


def _annotation_name(annotation: ast.AST | None) -> str | None:
    if annotation is None:
        return None
    if isinstance(annotation, ast.Name):
        return annotation.id
    if isinstance(annotation, ast.Attribute):
        return annotation.attr
    if isinstance(annotation, ast.Subscript):
        # Handle simple generic wrappers like Optional[Type]
        return _annotation_name(annotation.value)
    return None


def build_self_attr_type_map(init_node: ast.FunctionDef) -> dict[str, str]:
    mapping: dict[str, str] = {}

    # 1) Build parameter type map from __init__ signature annotations
    param_types: dict[str, str] = {}
    for arg in init_node.args.args:
        if arg.arg == "self":
            continue
        ann_name = _annotation_name(arg.annotation)
        if ann_name:
            param_types[arg.arg] = ann_name

    # 2) Infer self.attr type from assignments in body
    for stmt in ast.walk(init_node):
        if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
            continue
        target = stmt.targets[0]
        if not (
            isinstance(target, ast.Attribute)
            and isinstance(target.value, ast.Name)
            and target.value.id == "self"
        ):
            continue

        # self.x = SomeClass(...)
        if isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Name):
            mapping[target.attr] = stmt.value.func.id
            continue

        # self.x = constructor_param  where constructor_param: SomeClass
        if isinstance(stmt.value, ast.Name):
            param_type = param_types.get(stmt.value.id)
            if param_type:
                mapping[target.attr] = param_type
    return mapping


def collect_cross_module_edges() -> tuple[set[tuple[str, str]], dict[str, MethodRef]]:
    all_methods: dict[str, MethodRef] = {}
    class_module_methods: dict[tuple[str, str], set[str]] = {}
    module_ast_maps: dict[str, dict[tuple[str, str], ast.FunctionDef]] = {}

    for mod_file in MODULE_FILES:
        methods, ast_map = parse_methods(mod_file)
        all_methods.update(methods)
        module_ast_maps[mod_file.stem] = ast_map
        for m in methods.values():
            class_module_methods.setdefault((m.module, m.cls), set()).add(m.method)

    # map class name -> method symbols (possibly across modules)
    class_to_symbols: dict[str, list[str]] = {}
    for sym, ref in all_methods.items():
        class_to_symbols.setdefault(ref.cls, []).append(sym)

    edges: set[tuple[str, str]] = set()

    for src_sym, src_ref in all_methods.items():
        ast_map = module_ast_maps[src_ref.module]
        src_node = ast_map[(src_ref.cls, src_ref.method)]

        # determine self attribute class mapping via class __init__
        attr_type_map: dict[str, str] = {}
        init_node = ast_map.get((src_ref.cls, "__init__"))
        if init_node is not None:
            attr_type_map = build_self_attr_type_map(init_node)

        local_methods = class_module_methods.get((src_ref.module, src_ref.cls), set())

        for node in ast.walk(src_node):
            if not isinstance(node, ast.Call):
                continue
            func = node.func

            # self.method()
            if (
                isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == "self"
                and func.attr in local_methods
            ):
                dst = f"{src_ref.module}.{src_ref.cls}.{func.attr}"
                if dst in all_methods and all_methods[dst].module != src_ref.module:
                    edges.add((src_sym, dst))
                continue

            # self.attr.method() where attr set in __init__
            if (
                isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Attribute)
                and isinstance(func.value.value, ast.Name)
                and func.value.value.id == "self"
            ):
                attr_name = func.value.attr
                target_cls = attr_type_map.get(attr_name)
                if not target_cls:
                    continue

                candidates = [
                    sym for sym in class_to_symbols.get(target_cls, [])
                    if sym.endswith(f".{target_cls}.{func.attr}")
                ]

                # keep only unambiguous matches
                if len(candidates) == 1:
                    dst = candidates[0]
                    if all_methods[dst].module != src_ref.module:
                        edges.add((src_sym, dst))

    return edges, all_methods


def write_dot(edges: set[tuple[str, str]], methods: dict[str, MethodRef], out_path: Path) -> None:
    lines: list[str] = [
        "digraph StreetRaceCrossModuleCallGraph {",
        "  rankdir=TB;",
        "  node [shape=box, fontsize=10];",
        "  splines=true;",
    ]

    # only nodes that participate in cross-module edges
    used_nodes: set[str] = set()
    for src, dst in edges:
        used_nodes.add(src)
        used_nodes.add(dst)

    by_module: dict[str, list[str]] = {}
    for node in sorted(used_nodes):
        module = node.split(".", 1)[0]
        by_module.setdefault(module, []).append(node)

    for module, symbols in sorted(by_module.items()):
        lines.append(f'  subgraph "cluster_{module}" {{')
        lines.append(f'    label="{module}";')
        lines.append("    color=lightblue;")
        for sym in sorted(symbols):
            lines.append(f'    "{sym}";')
        lines.append("  }")

    for src, dst in sorted(edges):
        lines.append(f'  "{src}" -> "{dst}";')

    lines.append("}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    edges, methods = collect_cross_module_edges()
    dot_path = ROOT / "call_graph_v2.dot"
    png_path = ROOT / "call_graph_v2.png"

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
