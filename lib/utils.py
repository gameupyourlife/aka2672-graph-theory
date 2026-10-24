"""Small helper functions that are used throughout the course.

* :func:`load_exercise` - import ``task.py`` or ``demo_solution.py`` of another
  exercise (the folder names start with digits, so a normal ``import`` does
  not work).
* :func:`path_weight`, :func:`format_path` - work with paths given as lists.
* :func:`measure_time` - simple runtime measurements.
"""

from __future__ import annotations

import importlib.util
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from types import ModuleType
from typing import Any

from lib.graph import Graph, Vertex

PROJECT_ROOT = Path(__file__).resolve().parent.parent
"""Root folder of the course project."""

EXERCISES_DIR = PROJECT_ROOT / "exercises"
"""Folder that contains the exercise units."""


def load_module_from_path(path: str | Path, module_name: str | None = None) -> ModuleType:
    """Import the Python file at ``path`` and return it as a module.

    The module is cached in ``sys.modules``: loading the same file twice
    returns the same module object.

    Args:
        path: Path to a ``.py`` file.
        module_name: Name under which the module is registered. By default a
            unique name is derived from the path.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    if module_name is None:
        relative = path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path
        cleaned = "".join(c if c.isalnum() else "_" for c in str(relative.with_suffix("")))
        module_name = f"course_{cleaned}"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        del sys.modules[module_name]
        raise
    return module


def load_exercise(unit: str, module: str = "demo_solution") -> ModuleType:
    """Import a module of an exercise unit.

    Args:
        unit: Folder name of the unit, e.g. ``"02_bfs_dfs"``.
        module: ``"task"`` (your own solution) or ``"demo_solution"``.

    Example::

        bfs_dfs = load_exercise("02_bfs_dfs", "task")
        distance, parent = bfs_dfs.bfs(graph, "A")
    """
    return load_module_from_path(EXERCISES_DIR / unit / f"{module}.py")


def path_weight(graph: Graph, path: Sequence[Vertex]) -> float:
    """Return the sum of the edge weights along ``path``.

    A path with a single vertex has weight 0.

    Raises:
        ValueError: If the path is empty.
        KeyError: If two consecutive vertices are not joined by an edge.
    """
    if len(path) == 0:
        raise ValueError("The path is empty")
    return sum(graph.weight(path[i], path[i + 1]) for i in range(len(path) - 1))


def format_path(path: Sequence[Vertex] | None, directed: bool = True) -> str:
    """Return a path as a readable string, e.g. ``"A -> B -> C"``.

    ``None`` (no path exists) is shown as ``"(kein Weg)"``.
    """
    if path is None:
        return "(kein Weg)"
    separator = " -> " if directed else " - "
    return separator.join(str(v) for v in path)


def measure_time(function: Callable[..., Any], *args: Any, repeat: int = 3) -> float:
    """Call ``function(*args)`` ``repeat`` times and return the best time in seconds.

    Taking the minimum reduces the influence of other programs running on
    the computer.
    """
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        function(*args)
        best = min(best, time.perf_counter() - start)
    return best
