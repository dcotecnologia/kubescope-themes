import re

import pytest

import kubescope.theme_pack as package
from kubescope import theme
from kubescope.theme_pack import THEMES, activate, themes

ALL = themes()


def test_the_package_has_the_themes_of_the_app_that_are_not_light_and_dark() -> None:
    assert sorted(ALL) == [
        "abyss",
        "dark-modern",
        "high-contrast",
        "light-modern",
        "macos-dark",
        "macos-light",
        "midnight",
        "monokai",
        "quiet-light",
        "sepia",
        "solarized-dark",
        "solarized-light",
        "tomorrow-night-blue",
    ]
    assert not {"light", "dark"} & set(ALL)  # those are built in


@pytest.mark.parametrize("theme_id", sorted(ALL))
def test_every_theme_is_valid_for_the_app(theme_id) -> None:
    parsed = theme.parse_theme(theme_id, ALL[theme_id])

    assert parsed.name.strip() and parsed.base in ("light", "dark")
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", theme_id)  # a short, lowercase id


def test_the_names_are_unique() -> None:
    names = [document["name"] for document in ALL.values()]

    assert len(set(names)) == len(names)


def luminance(color: str) -> float:
    channels = [int(color[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [
        c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


@pytest.mark.parametrize("theme_id", sorted(ALL))
def test_the_text_is_readable_on_the_page(theme_id) -> None:
    colors = theme.parse_theme(theme_id, ALL[theme_id]).colors
    text, page = luminance(colors["#20232a"]), luminance(colors["#f7f7fa"])
    ratio = (max(text, page) + 0.05) / (min(text, page) + 0.05)

    assert ratio >= 4.5, f"{theme_id}: {ratio:.1f}:1"


def test_the_extension_offers_each_theme(ctx) -> None:
    activate(ctx)  # type: ignore[arg-type]

    assert ctx.themes == ALL


def test_the_themes_are_files_next_to_the_code() -> None:
    assert THEMES.is_dir() and THEMES.name == "themes"
    assert package.THEMES == THEMES
