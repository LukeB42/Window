#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fit_align_expand.py — demo of FIT, EXPAND, ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER.

Layout (top → bottom)
─────────────────────
  [HEADER — 1 row, EXPAND width, ALIGN_CENTER]
  [LEFT pane — FIT width]  [RIGHT pane — EXPAND width]
  [STATUS bar — 1 row, EXPAND width, ALIGN_RIGHT]

Press ← / → to cycle through alignments on the right pane.
Press q or ^Q to quit.
"""
import sys
sys.path.insert(0, '..')
from window import *


ALIGNMENTS = [ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT]
ALIGN_NAMES = {ALIGN_LEFT: "ALIGN_LEFT", ALIGN_CENTER: "ALIGN_CENTER", ALIGN_RIGHT: "ALIGN_RIGHT"}

LOREM = (
    "Lorem ipsum dolor sit amet.\n"
    "Consectetur adipiscing elit.\n"
    "Sed do eiusmod tempor incididunt.\n"
    "\n"
    "UTF-8 bonus:\n"
    "  日本語  Ελληνικά  Русский\n"
    "  ♩ ♪ ♫ ♬  ∑ ∫ π ≠ ∞\n"
    "  🎹 🎸 🥁 🎺\n"
)


class Header(Pane):
    """Single-row centred header — geometry uses EXPAND width, fixed height 1."""
    geometry = [EXPAND, 1]

    def update(self):
        title = " FIT / ALIGN / EXPAND demo — ← → cycle alignment, q quit "
        self.change_content(0, title, ALIGN_CENTER, palette("black", "white"))


class LeftPane(Pane):
    """
    FIT width: the pane is exactly as wide as its widest content line.
    Fixed height via EXPAND so it fills the vertical space.
    """
    geometry = [FIT, EXPAND]

    def update(self):
        label = "◀ FIT width ▶\n"
        self.change_content(0, label,  ALIGN_LEFT, palette("white", "blue"))
        self.change_content(1, LOREM,  ALIGN_LEFT)
        dim = "h=%s w=%s" % (self.height, self.width)
        self.change_content(2, dim, ALIGN_LEFT, palette("black", "cyan"))


class RightPane(Pane):
    """
    EXPAND width: fills the space the FIT pane didn't claim.
    Alignment cycles via ← / → keys.
    """
    geometry = [EXPAND, EXPAND]
    _align_idx = 0

    def update(self):
        align = ALIGNMENTS[self._align_idx]
        label = "◀ EXPAND width — %s ▶\n" % ALIGN_NAMES[align]
        self.change_content(0, label, ALIGN_CENTER, palette("white", "blue"))
        self.change_content(1, LOREM, align)
        dim = "h=%s w=%s" % (self.height, self.width)
        self.change_content(2, dim, ALIGN_RIGHT, palette("black", "cyan"))

    def process_input(self, character):
        if character in (260, ord('h')):   # ←
            self._align_idx = (self._align_idx - 1) % len(ALIGNMENTS)
            self.window.window.clear()
        elif character in (261, ord('l')): # →
            self._align_idx = (self._align_idx + 1) % len(ALIGNMENTS)
            self.window.window.clear()


class StatusBar(Pane):
    """Single-row status bar, text flushed right."""
    geometry = [EXPAND, 1]

    def update(self):
        msg = "Python %d.%d.%d  |  window.py %s  |  q to quit " % (
            sys.version_info.major, sys.version_info.minor, sys.version_info.micro,
            VERSION,
        )
        self.change_content(0, msg, ALIGN_RIGHT, palette("black", "white"))


if __name__ == "__main__":
    window = Window(blocking=True)

    header = Header("header")
    left   = LeftPane("left")
    right  = RightPane("right")
    status = StatusBar("status")

    window.add(header)
    window.add([left, right])   # side-by-side on the same row
    window.add(status)

    window.exit_keys.append(ord('q'))
    window.exit_keys.append(17)   # ^Q

    try:
        window.start()
    except KeyboardInterrupt:
        pass
