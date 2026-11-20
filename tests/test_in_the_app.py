"""The extension in the window of the app, with the real services lent to
it."""

import time

import pytest
from kubescope.extensions.context import ExtensionContext
from PySide6.QtWidgets import QApplication

from kubescope import theme
from kubescope.theme_pack import activate, themes


@pytest.fixture
def window(monkeypatch):
    from kubescope import window as window_module

    application = QApplication.instance() or QApplication([])
    # the window downloads the extensions the app recommends on its first run
    monkeypatch.setattr("kubescope.extensions.defaults.DEFAULTS", ())
    monkeypatch.setattr(window_module, "list_contexts", lambda: ([], None))
    monkeypatch.setattr(
        window_module.WorkloadWindow, "refresh_overview", lambda *_a: None
    )
    shown = window_module.WorkloadWindow()
    deadline = time.monotonic() + 10
    while shown._action_workers and time.monotonic() < deadline:
        application.processEvents()
        time.sleep(0.005)
    yield shown
    shown.close()
    theme.set_contributed_themes([])
    theme.set_theme("light")


def test_the_themes_are_in_the_settings_and_the_one_chosen_is_put_on(window) -> None:
    window.settings.theme = "midnight"  # chosen before the extension ran
    window._apply_theme()
    assert theme.active_theme() == "dark"  # it did not exist yet: the default
    context = ExtensionContext(
        "kubescope.themes", frozenset({"ui.theme"}), window.extension_host
    )

    activate(context)
    window._apply_extension_contributions()

    combo = window.settings_ui.themeCombo
    shown = [combo.itemData(row) for row in range(combo.count())]
    assert shown[:2] == ["light", "dark"] and set(themes()) <= set(shown)
    assert theme.active_theme() == "midnight"  # as soon as it exists
    assert combo.currentData() == "midnight"
    assert not theme.can_delete_theme("midnight")  # it goes with the extension

    context.close()
    window._apply_extension_contributions()
    assert theme.active_theme() == "dark"  # the extension is gone: the default
