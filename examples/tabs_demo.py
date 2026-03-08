#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tabs_demo.py — demonstrates TabBar: a single-row menu of titles that swaps
               a single pane of focus, providing a tabs-like interface.

Layout
──────
  ┌──────────────────────────────────────────────────────┐
  │  Alpha  │  Beta  │  Gamma  │  Delta                  │  ← TabBar (1 row)
  ├──────────────────────────────────────────────────────┤
  │                                                      │
  │   (content pane for the active tab)                  │  ← EXPAND
  │                                                      │
  └──────────────────────────────────────────────────────┘

Navigation
──────────
  ← / h      previous tab
  → / l      next tab
  Tab / Enter / Space   activate highlighted tab
  q or ^Q    quit
"""
import sys
sys.path.insert(0, '..')
from window import *


# ── Per-tab content panes ────────────────────────────────────────────────────

class AlphaPane(Pane):
    geometry = [EXPAND, EXPAND]

    def update(self):
        body = (
            "  Alpha tab\n\n"
            "  This pane demonstrates ALIGN_LEFT (default).\n\n"
            "  UTF-8 sampler:\n"
            "    日本語: 東京  |  한국어: 서울  |  中文: 北京\n"
            "    Arabic: مرحبا  |  Hebrew: שלום\n"
            "    Math: ∑ ∫ ∂ √ ∞ π ≈ ≠ ≤ ≥\n"
            "    Music: ♩ ♪ ♫ ♬ 𝄞 𝄢\n"
            "    Emoji: 🎹 🎸 🥁 🎷 🎺 🎻\n"
        )
        self.change_content(0, body, ALIGN_LEFT)


class BetaPane(Pane):
    geometry = [EXPAND, EXPAND]
    _tick = 0

    def update(self):
        self._tick += 1
        body = (
            "  Beta tab — live counter\n\n"
            "  ALIGN_CENTER demo:\n\n"
            "  Redraw #%d\n\n"
            "  The content of this pane is centred within\n"
            "  the available width on every line.\n"
        ) % self._tick
        self.change_content(0, body, ALIGN_CENTER, palette("white", -1))


class GammaPane(Pane):
    geometry = [EXPAND, EXPAND]

    def update(self):
        body = (
            "  Gamma tab\n\n"
            "  ALIGN_RIGHT demo.\n\n"
            "  Each line of this pane is flush-right.\n\n"
            "  Resize the terminal to watch it reflow.\n"
        )
        self.change_content(0, body, ALIGN_RIGHT)


class DeltaPane(Pane):
    """Interactive pager."""
    geometry = [EXPAND, EXPAND]

    _TEXT = "\n".join(
        ["  Delta tab — scrollable pager  (↑↓ / PgUp PgDn to scroll)"]
        + [""]
        + ["  Line %3d: %s" % (i, "█" * (i % 40)) for i in range(1, 80)]
    )

    _pos = 0

    def update(self):
        lines = self._TEXT.split('\n')[self._pos:]
        self.change_content(0, '\n'.join(lines))

    def process_input(self, character):
        total = len(self._TEXT.split('\n'))
        self.window.window.clear()
        if character == 259:           # ↑
            self._pos = max(0, self._pos - 1)
        elif character == 258:         # ↓
            if self._pos + 1 < total:
                self._pos += 1
        elif character == 339:         # PgUp
            self._pos = max(0, self._pos - (self.height or 10))
        elif character == 338:         # PgDn
            if self._pos + (self.height or 10) < total:
                self._pos += (self.height or 10)


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    window = Window(blocking=True)

    # The TabBar sits at the top — height 1, full width
    bar = TabBar("tabbar")

    # Content panes — all stacked vertically in window.panes,
    # but only the active one is visible at a time
    alpha = AlphaPane("alpha")
    beta  = BetaPane("beta")
    gamma = GammaPane("gamma")
    delta = DeltaPane("delta")

    window.add(bar)
    window.add(alpha)
    window.add(beta)
    window.add(gamma)
    window.add(delta)

    # Register tabs *after* window.add() so pane objects are fully initialised
    bar.register("Alpha", alpha)
    bar.register("Beta",  beta)
    bar.register("Gamma", gamma)
    bar.register("Delta", delta)

    # Show tab 0, hide the rest
    bar.select(0)

    # TabBar handles input; content pane handles its own input when active.
    # Both need to be active simultaneously so route input to both.
    # The TabBar will deactivate non-selected content panes via select().
    # We leave content panes' active state managed by bar.select().

    window.exit_keys.append(ord('q'))
    window.exit_keys.append(17)   # ^Q

    try:
        window.start()
    except KeyboardInterrupt:
        pass
