import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"


def imports_of_kubescope(path: Path) -> list[str]:
    found: list[str] = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.ImportFrom) and node.module:
            parts = node.module.split(".")
            if parts[0] == "kubescope":
                if len(parts) == 1:
                    found += [f"kubescope.{alias.name}" for alias in node.names]
                else:
                    found.append(node.module)
        elif isinstance(node, ast.Import):
            found += [a.name for a in node.names if a.name.split(".")[0] == "kubescope"]
    return found


def test_it_imports_nothing_of_kubescope_but_the_sdk_and_itself() -> None:
    """It is written against the SDK, so it can be installed and run without
    the app being importable."""
    offenders = [
        f"{path.relative_to(SRC)}: {name}"
        for path in sorted(SRC.rglob("*.py"))
        for name in imports_of_kubescope(path)
        if name.split(".")[:2]
        not in (["kubescope", "sdk"], ["kubescope", "theme_pack"])
    ]

    assert offenders == []


def test_its_modules_are_all_found() -> None:
    assert len(list(SRC.rglob("*.py"))) >= 1
