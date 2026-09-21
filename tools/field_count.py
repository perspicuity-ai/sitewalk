#!/usr/bin/env python3
"""Count the declared fields of the package, so a number in the record can be reproduced.

    python3 tools/field_count.py [--revision REV]

This exists because a field count was published twice in `RECORD.md` and neither version
reproduced, which is the defect class the project keeps finding: a claim in the record that the
code does not support. A number nobody can re-derive is not evidence.

Method, stated so a reader can disagree with it rather than with the arithmetic:

* **dataclass fields** — annotated names in the body of a class decorated with `@dataclass`,
  in any decorator form (`@dataclass`, `@dataclass(frozen=True)`).
* **protocol annotations** — annotated names in the body of a class decorated with `@Protocol`.
* Counted over `sitewalk/` **and** `tests/`, because a test double is a declaration of the same
  interface and changed the net between revisions.
* Underscore-prefixed names are excluded: they are implementation state, not declared fields.

The count is a maintenance signal, not a criterion. What matters is that it is the same number
whenever two people run it.
"""

from __future__ import annotations

import argparse
import ast
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent


def decorator_names(cls: ast.ClassDef) -> set[str]:
    """Decorators *and* bases, because `class X(Protocol)` is as common as `@dataclass`.

    A first version of this script looked only at decorators and reported zero protocol fields,
    which is how a counting script quietly changes the answer. Bases are read for the same names.
    """
    names = set()
    for decorator in cls.decorator_list:
        if isinstance(decorator, ast.Name):
            names.add(decorator.id)
        elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
            names.add(decorator.func.id)
    for base in cls.bases:
        if isinstance(base, ast.Name):
            names.add(base.id)
        elif isinstance(base, ast.Subscript) and isinstance(base.value, ast.Name):
            names.add(base.value.id)
    return names


def count(root: pathlib.Path) -> dict[str, int]:
    totals = {"dataclass": 0, "protocol": 0}
    for path in sorted((root / "sitewalk").glob("*.py")) + sorted((root / "tests").glob("*.py")):
        for cls in [n for n in ast.parse(path.read_text()).body if isinstance(n, ast.ClassDef)]:
            names = [
                statement.target.id
                for statement in cls.body
                if isinstance(statement, ast.AnnAssign)
                and isinstance(statement.target, ast.Name)
                and not statement.target.id.startswith("_")
            ]
            decorators = decorator_names(cls)
            if "dataclass" in decorators:
                totals["dataclass"] += len(names)
            elif "Protocol" in decorators:
                totals["protocol"] += len(names)
    totals["total"] = totals["dataclass"] + totals["protocol"]
    return totals


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", help="count a git revision instead of the working tree")
    args = parser.parse_args(argv)

    if args.revision:
        with tempfile.TemporaryDirectory() as temporary:
            worktree = pathlib.Path(temporary) / "rev"
            subprocess.run(
                ["git", "worktree", "add", "-q", "--detach", str(worktree), args.revision],
                cwd=ROOT,
                check=True,
            )
            try:
                totals = count(worktree)
            finally:
                subprocess.run(
                    ["git", "worktree", "remove", "--force", str(worktree)], cwd=ROOT, check=True
                )
    else:
        totals = count(ROOT)

    label = args.revision or "working tree"
    print(
        f"{label}: {totals['total']} fields "
        f"({totals['dataclass']} dataclass + {totals['protocol']} protocol)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
