#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kilo.py — a minimal text editor built on window.py

Demonstrates UTF-8 support: the initial buffer contains Japanese, Arabic,
Russian, emoji and full-width CJK characters so you can verify that
arbitrary Unicode renders correctly and that backspace removes whole
code-points (not bytes).

Controls
--------
^X  quit          ^O  save to file
^W  delete word   ^K  yank (cut) line
^A  run last line as shell command
"""
import os
import sys
import subprocess
from window import *


# Seed buffer with multi-script UTF-8 text so the UTF-8 path is exercised
# immediately on launch.
UTF8_SAMPLE = (
    "# UTF-8 test — edit freely, ^X to quit\n"
    "日本語: 東京タワー  (Japanese full-width + kana)\n"
    "العربية: مرحبا بالعالم     (Arabic RTL — rendered LTR in terminal)\n"
    "Русский: Привет, мир!      (Cyrillic)\n"
    "Emoji:   🎹 🎸 🥁 🎷 🎺  (multi-byte emoji)\n"
    "Math:    ∑ ∫ ∂ √ ∞ π ≈ ≠ ≤ ≥\n"
    "Music:   ♩ ♪ ♫ ♬ 𝄞 𝄢\n"
    "\n"
)


class Editor(Pane):
    """
    Text editor pane.

    Bindings
    --------
    ^X  exit          ^O  save
    ^W  delete word   ^K  yank line
    ^A  run last line as shell command
    """
    geometry  = [EXPAND, EXPAND]
    buffer    = UTF8_SAMPLE
    clipboard = ""

    def update(self):
        header = "  Psybernetics kilo 0.0.2 (Python %d.%d.%d)" % (
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro,
        )
        header += ' ' * max(0, self.width - len(header))
        header += "\n"
        self.change_content(0, header, ALIGN_LEFT, palette("black", "white"))

    def process_input(self, character):
        self.window.window.clear()
        self.status.change_content(0, str(character), ALIGN_LEFT, palette(-1, -1))

        if character == 23 and self.buffer:       # ^W — delete word
            lines = self.buffer.split("\n")
            words = lines[-1].split()
            lines[-1] = ' '.join(words[:-1])
            self.buffer = '\n'.join(lines)

        elif character == 11 and self.buffer:     # ^K — yank line
            lines = self.buffer.split("\n")
            self.clipboard = lines[-1]
            self.buffer = '\n'.join(lines[:-1])

        elif character == 15 and self.buffer:     # ^O — save
            self.active = False
            self.status.saving = True

        elif character == 263 and self.buffer:    # Backspace — pop one code-point
            self.buffer = self.buffer[:-1]

        elif character in (10, 13):               # Enter
            self.buffer += "\n"

        elif character == 1:                      # ^A — run last line as shell cmd
            line = self.buffer.split('\n')[-1].split()
            if line:
                try:
                    output = subprocess.Popen(
                        line, stdout=subprocess.PIPE
                    ).communicate()[0]
                    lines = self.buffer.split('\n')
                    lines[-1] = output.decode("utf-8", "replace")
                    self.buffer = '\n'.join(lines)
                except Exception:
                    pass
        else:
            try:
                self.buffer += chr(character)
            except Exception:
                pass

        self.change_content(1, self.buffer, ALIGN_LEFT)
        self.change_content(2, ' ', ALIGN_LEFT, palette(-1, "yellow"))


class Status(Pane):
    geometry = [EXPAND, 1]
    saving   = False
    buffer   = ""

    def update(self):
        if not self.saving:
            self._compute_status_line()

    def process_input(self, character):
        if not self.saving:
            return
        self.window.window.clear()
        if character == 263 and self.buffer:     # Backspace
            self.buffer = self.buffer[:-1]
        elif character in (10, 13):              # Enter — write file
            path = os.path.expanduser(self.buffer)
            try:
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write(self.editor.buffer)
            except OSError as e:
                pass
            self.buffer = ""
            self.saving = False
            self.editor.active = True
        else:
            try:
                self.buffer += chr(character)
            except Exception:
                pass
        line  = "Filename: " + self.buffer
        line += ' ' * max(0, self.width - len(line))
        self.change_content(0, line, ALIGN_LEFT, palette("black", "white"))

    def _compute_status_line(self):
        parts = []
        c = len(self.editor.buffer)
        if c:
            parts.append("C%d" % c)
        w = len(self.editor.buffer.split())
        if w:
            parts.append("W%d" % w)
        lc = len(self.editor.buffer.split('\n'))
        if lc:
            parts.append("L%d" % lc)
        info   = ", ".join(parts)
        filler = ' ' * max(0, (self.width // 2) - (len(info) // 2))
        line   = filler + info
        line  += ' ' * max(0, self.width - len(line))
        self.change_content(0, line, ALIGN_LEFT, palette("black", "white"))


if __name__ == "__main__":
    window = Window()
    editor = Editor("editor")
    status = Status("status")
    editor.status = status
    status.editor = editor
    window.add(editor)
    window.add(status)
    window.exit_keys.append(24)   # ^X to quit
    try:
        window.start()
    except KeyboardInterrupt:
        pass
