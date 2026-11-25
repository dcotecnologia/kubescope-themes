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


def test_it_imports_no_qt_class_but_takes_them_from_the_sdk() -> None:
    """The widgets, timers, icons and the rest of Qt come through
    `ctx.ui.components` (see the Components guide of the SDK), in the code and
    in the tests, so a change to the look of the app reaches the extension
    without a line of it."""
    tests = Path(__file__).resolve().parent
    offenders = []
    for path in sorted([*SRC.rglob("*.py"), *tests.rglob("*.py")]):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            names = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            elif isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            offenders += [
                f"{path.name}: {name}"
                for name in names
                if name.split(".")[0] in ("PySide6", "shiboken6")
                and not path.name.startswith("ui_")
            ]
    assert offenders == []
