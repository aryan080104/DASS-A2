"""Generate a third call graph view: module-level interaction graph.

Usage:
    python streetrace_manager/generate_call_graph_v3.py

Outputs:
    - streetrace_manager/call_graph_v3.dot
    - streetrace_manager/call_graph_v3.png

This view collapses function calls into module-to-module edges so you can
cross-check architecture-level interactions.
"""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path


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
    }
)


def parse_class_methods(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    module = path.stem
    classes: dict[str, dict[str, ast.FunctionDef]] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = {}
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    methods[child.name] = child
            classes[node.name] = methods
    return module, classes


def ann_name(annotation: ast.AST | None) -> str | None:
    if annotation is None:
        return None
    if isinstance(annotation, ast.Name):
        return annotation.id
    if isinstance(annotation, ast.Attribute):
        return annotation.attr
    if isinstance(annotation, ast.Subscript):
        return ann_name(annotation.value)
    return None


def build_self_attr_types(init_fn: ast.FunctionDef) -> dict[str, str]:
    param_types: dict[str, str] = {}
    for arg in init_fn.args.args:
        if arg.arg == "self":
            continue
        name = ann_name(arg.annotation)
        if name:
            param_types[arg.arg] = name

    attr_types: dict[str, str] = {}
    for stmt in ast.walk(init_fn):
        if not isinstance(stmt, ast.Assign) or len(stmt.targets) != 1:
            continue
        target = stmt.targets[0]
        if not (
            isinstance(target, ast.Attribute)
            and isinstance(target.value, ast.Name)
            and target.value.id == "self"
        ):
            continue

        if isinstance(stmt.value, ast.Call) and isinstance(stmt.value.func, ast.Name):
            attr_types[target.attr] = stmt.value.func.id
            continue

        if isinstance(stmt.value, ast.Name):
            ptype = param_types.get(stmt.value.id)
            if ptype:
                attr_types[target.attr] = ptype

    return attr_types


def main() -> None:
    module_class_methods: dict[str, dict[str, dict[str, ast.FunctionDef]]] = {}
    class_to_module: dict[str, str] = {}

    for f in MODULE_FILES:
        module, classes = parse_class_methods(f)
        module_class_methods[module] = classes
        for cls_name in classes:
            class_to_module[cls_name] = module

    module_edges: set[tuple[str, str]] = set()

    for src_module, classes in module_class_methods.items():
        for cls_name, methods in classes.items():
            init_fn = methods.get("__init__")
            attr_types = build_self_attr_types(init_fn) if init_fn else {}

            for _method_name, fn in methods.items():
                for node in ast.walk(fn):
                    if not isinstance(node, ast.Call):
                        continue
                    func = node.func

                    # self.<attr>.<method>()
                    if (
                        isinstance(func, ast.Attribute)
                        and isinstance(func.value, ast.Attribute)
                        and isinstance(func.value.value, ast.Name)
                        and func.value.value.id == "self"
                    ):
                        attr = func.value.attr
                        target_class = attr_types.get(attr)
                        if target_class and target_class in class_to_module:
                            dst_module = class_to_module[target_class]
                            if dst_module != src_module:
                                module_edges.add((src_module, dst_module))

    dot_path = ROOT / "call_graph_v3.dot"
    png_path = ROOT / "call_graph_v3.png"

    lines = [
        "digraph StreetRaceModuleInteractions {",
        "  rankdir=LR;",
        "  node [shape=ellipse, style=filled, fillcolor=lightgoldenrod1];",
    ]

    modules = sorted(module_class_methods.keys())
    for m in modules:
        lines.append(f'  "{m}";')

    for src, dst in sorted(module_edges):
        lines.append(f'  "{src}" -> "{dst}";')

    lines.append("}")
    dot_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    try:
        subprocess.run(["dot", "-Tpng", str(dot_path), "-o", str(png_path)], check=True)
        print(f"Generated: {dot_path}")
        print(f"Generated: {png_path}")
    except Exception:
        print(f"Generated: {dot_path}")
        print("Could not render PNG. Ensure Graphviz is installed.")


if __name__ == "__main__":
    main()
