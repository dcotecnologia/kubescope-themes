"""Fixtures of the tests of the themes."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Never read or write the real user settings during tests."""
    monkeypatch.setenv("KUBESCOPE_CONFIG_DIR", str(tmp_path / "config"))
    home = tmp_path / "isolated-home"
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))


class FakeCtx:
    """What the app gives the extension, in the hands of the test."""

    id = "kubescope.themes"
    permissions = frozenset({"ui.theme"})

    def __init__(self) -> None:
        self.themes: dict[str, dict] = {}

    def add_theme(self, theme_id, document) -> None:
        self.themes[theme_id] = dict(document)


@pytest.fixture
def ctx():
    return FakeCtx()
