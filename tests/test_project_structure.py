"""Quality checks for the course material itself.

These tests make sure that every unit is complete: all four files exist,
README.md has the nine required sections, task.py contains TODOs instead of
solutions, and every Python file can be parsed.
"""

import ast
from pathlib import Path

import pytest

from lib.utils import EXERCISES_DIR, PROJECT_ROOT

UNITS = sorted(p for p in EXERCISES_DIR.iterdir() if p.is_dir() and p.name[:2].isdigit())

# The student version (tools/make_student_version.py) ships without demo solutions.
HAS_DEMOS = any((unit / "demo_solution.py").exists() for unit in UNITS)
needs_demos = pytest.mark.skipif(not HAS_DEMOS, reason="student version without demo solutions")

README_SECTIONS = [
    "## 1. Titel und Lernziele",
    "## 2. Mathematischer Hintergrund",
    "## 3. Relevante Definitionen",
    "## 4. Problemstellung",
    "## 5. Arbeitsaufträge",
    "## 6. Anforderungen an die Implementierung",
    "## 7. Beispiele für erwartetes Verhalten",
    "## 8. Hinweise und optionale Zusatzaufgaben",
    "## 9. Quellen und weiterführende Literatur",
]


def test_there_are_ten_units() -> None:
    assert [u.name[:2] for u in UNITS] == [f"{i:02d}" for i in range(1, 11)]


@pytest.mark.parametrize("unit", UNITS, ids=lambda p: p.name)
def test_unit_has_all_files(unit: Path) -> None:
    required = ["README.md", "task.py", "test_task.py"] + (["demo_solution.py"] if HAS_DEMOS else [])
    for name in required:
        assert (unit / name).is_file(), f"{unit.name}/{name} is missing"


@pytest.mark.parametrize("unit", UNITS, ids=lambda p: p.name)
def test_readme_has_all_sections(unit: Path) -> None:
    text = (unit / "README.md").read_text(encoding="utf-8")
    positions = []
    for section in README_SECTIONS:
        assert section in text, f"{unit.name}/README.md lacks '{section}'"
        positions.append(text.index(section))
    assert positions == sorted(positions), "sections are out of order"


def public_functions(path: Path) -> dict[str, ast.FunctionDef]:
    """Return all public top-level functions and public methods of public classes."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    result: dict[str, ast.FunctionDef] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_") and node.name != "main":
            result[node.name] = node
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and (not item.name.startswith("_") or item.name == "__init__"):
                    result[f"{node.name}.{item.name}"] = item
    return result


@pytest.mark.parametrize("unit", UNITS, ids=lambda p: p.name)
def test_task_contains_only_todos(unit: Path) -> None:
    task = unit / "task.py"
    text = task.read_text(encoding="utf-8")
    assert "TODO" in text
    functions = public_functions(task)
    assert functions, "task.py defines no functions"
    for name, node in functions.items():
        assert ast.get_docstring(node), f"{name} has no docstring"
        raises = [
            n for n in ast.walk(node)
            if isinstance(n, ast.Raise) and "NotImplementedError" in ast.unparse(n)
        ]
        assert raises, f"task.py: {name} does not raise NotImplementedError (solution leaked?)"
        # Apart from the docstring, the body must consist of the raise only.
        body = node.body[1:] if ast.get_docstring(node) else node.body
        assert len(body) == 1 and isinstance(body[0], ast.Raise), (
            f"task.py: {name} contains code besides 'raise NotImplementedError'"
        )


@needs_demos
@pytest.mark.parametrize("unit", UNITS, ids=lambda p: p.name)
def test_task_and_demo_have_same_interface(unit: Path) -> None:
    task = public_functions(unit / "task.py")
    demo = public_functions(unit / "demo_solution.py")
    assert set(task) == set(demo)
    for name in task:
        assert ast.unparse(task[name].args) == ast.unparse(demo[name].args), f"signature of {name} differs"
        assert ast.unparse(task[name].returns or ast.Constant(None)) == ast.unparse(
            demo[name].returns or ast.Constant(None)
        ), f"return type of {name} differs"


@pytest.mark.parametrize("unit", UNITS, ids=lambda p: p.name)
def test_public_functions_are_typed_and_documented(unit: Path) -> None:
    for name, node in public_functions(unit / "task.py").items():
        assert ast.get_docstring(node), f"{name} has no docstring"
        assert node.returns is not None, f"{name} has no return type hint"
        for arg in node.args.args:
            if arg.arg != "self":
                assert arg.annotation is not None, f"{name}: argument {arg.arg} has no type hint"


def test_all_python_files_parse() -> None:
    for path in PROJECT_ROOT.rglob("*.py"):
        if ".venv" in path.parts:
            continue
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
