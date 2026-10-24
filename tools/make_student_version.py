"""Create a ZIP file of the course for students - without the demo solutions.

Usage (from the project root)::

    python tools/make_student_version.py

The archive is written to ``dist/graphentheorie-kurs-studierende.zip``.
It contains everything except ``demo_solution.py`` files, virtual
environments, caches and the ``dist`` folder itself.
"""

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".venv", "venv", "__pycache__", ".pytest_cache", "dist", "build", ".git"}
EXCLUDED_FILES = {"demo_solution.py"}
EXCLUDED_SUFFIXES = {".pyc", ".dot", ".png"}


def student_files(root: Path) -> list[Path]:
    """Return all files that belong into the student version, sorted."""
    files = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRS or part.endswith(".egg-info") for part in relative.parts):
            continue
        if not path.is_file() or path.name in EXCLUDED_FILES or path.suffix in EXCLUDED_SUFFIXES:
            continue
        files.append(path)
    return sorted(files)


def main() -> None:
    """Write the ZIP archive and print a short summary."""
    target = ROOT / "dist" / "graphentheorie-kurs-studierende.zip"
    target.parent.mkdir(exist_ok=True)
    files = student_files(ROOT)
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, Path("graphentheorie-kurs") / path.relative_to(ROOT))
    print(f"Wrote {target} ({len(files)} files, without demo solutions)")


if __name__ == "__main__":
    sys.exit(main())
