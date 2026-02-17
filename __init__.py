from __future__ import annotations

from aqt import mw
from aqt.deckbrowser import DeckBrowser
from aqt.theme import Theme, theme_manager

__addon_name__ = "Theme Toggler"
__version__ = "1.0.0"

TOGGLE_CMD = "toggle-theme"
TOGGLE_LABEL = "Toggle Theme"
_PATCH_FLAG = "_theme_toggler_patched"


def _toggle_theme() -> None:
    if theme_manager.night_mode:
        mw.set_theme(Theme.LIGHT)
    else:
        mw.set_theme(Theme.DARK)
    if mw.state == "deckBrowser":
        mw.deckBrowser.refresh()


if not getattr(DeckBrowser, _PATCH_FLAG, False):
    setattr(DeckBrowser, _PATCH_FLAG, True)

    _original_link_handler = DeckBrowser._linkHandler

    def _linkHandler(self: DeckBrowser, url: str):
        if url == TOGGLE_CMD:
            _toggle_theme()
            return True
        return _original_link_handler(self, url)

    DeckBrowser._linkHandler = _linkHandler

    if not any(link[1] == TOGGLE_CMD for link in DeckBrowser.drawLinks):
        DeckBrowser.drawLinks.append(["", TOGGLE_CMD, TOGGLE_LABEL])
