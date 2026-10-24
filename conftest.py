"""pytest configuration for the whole course.

Adds the command line option ``--impl``:

* ``pytest``             - test your own solutions (``task.py``, default)
* ``pytest --impl=demo`` - test the demo solutions (``demo_solution.py``)
"""

import os

import pytest

from lib.testing import IMPLEMENTATION_ENV_VAR


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--impl",
        choices=["task", "demo"],
        default=None,
        help="which file the exercise tests use: task.py (default) or demo_solution.py",
    )


def pytest_configure(config: pytest.Config) -> None:
    choice = config.getoption("--impl")
    if choice is not None:
        os.environ[IMPLEMENTATION_ENV_VAR] = choice


def pytest_report_header(config: pytest.Config) -> str:
    choice = os.environ.get(IMPLEMENTATION_ENV_VAR, "task")
    filename = "demo_solution.py" if choice == "demo" else "task.py"
    return f"graph course: exercise tests check {filename}"
