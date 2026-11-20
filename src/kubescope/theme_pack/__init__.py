"""Color themes for KubeScope: the themes of the app that are not Light and
Dark."""

import json
from pathlib import Path

from kubescope.sdk import Context

THEMES = Path(__file__).resolve().parent / "themes"


def themes() -> dict[str, dict]:
    """The theme documents of this package, by id (the name of the file)."""
    return {
        path.stem: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(THEMES.glob("*.json"))
    }


def activate(ctx: Context) -> None:
    """What the app calls to run the extension: offer each theme."""
    for theme_id, document in themes().items():
        ctx.add_theme(theme_id, document)
