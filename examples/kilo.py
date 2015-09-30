#!/usr/bin/env python
import os
import subprocess
from window import *

class Editor(Pane):
	"""
	Defines a text editor/input pane.
	"""
	geometry = [EXPAND, EXPAND]
	buffer = ""
	buffers = {}
	clipboard = ""

	def update(self):

		header = "  Psybernetics kilo 0.0.1"
		header += ' ' * (self.width - len(header))
		header += "\n"
		self.change_content(0,header, ALIGN_LEFT, palette("black", "white"))
		pass
#		if len(self.content) >= 1:
#			self.change_content(1, "%i\n" % len(self.buffer))

	def process_input(self, character):
		self.window.window.clear()

		if character == 23 and self.buffer:        # Delete word on ^W
			self.buffer = self.buffer.split("\n")
			line = self.buffer[-1].split()
			if line:
				line = ' '.join(line[:-1])
			self.buffer[-1] = line
			self.buffer = '\n'.join(self.buffer)

		elif character == 11 and self.buffer:      # Yank line on ^K
			self.buffer = self.buffer.split("\n")
			self.clipboard = self.buffer[-1]
			self.buffer = '\n'.join(self.buffer[:-1])

		elif character == 15 and self.buffer:      # Write file to disk on ^O
			self.active = False
			self.status.saving = True
		elif character == 263 and self.buffer:     # Handle backspace
			self.buffer = self.buffer[:-1]
		elif character == 10 or character == 13:   # Handle the return key
			self.buffer += "\n"
		elif character == 1:                       # Execute as cmd on ^A
			line = self.buffer.split('\n')[-1]
			line = line.split()
			if not line: return
			output = subprocess.Popen(line, stdout=subprocess.PIPE).communicate()[0]
			self.buffer = self.buffer.split('\n')
			self.buffer[-1] = output
			self.buffer = '\n'.join(self.buffer)
		else:
			try: self.buffer += chr(character)     # Append input to buffer
			except: pass
		self.change_content(1, self.buffer, ALIGN_LEFT)
		self.change_content(2, ' ', ALIGN_LEFT, palette(-1, "yellow"))

class Status(Pane):
	geometry = [EXPAND, 1]
	col = ["black","white"]
#	col = ["white",-1]
	saving = False
	buffer = ""

	def update(self):
		if not self.saving:
			self.compute_status_line()

	def process_input(self, character):
		if self.saving:
			self.window.window.clear()
			if character == 15:
				pass
			elif character == 263 and self.buffer:     # Handle backspace
				self.buffer = self.buffer[:-1]
			elif character == 10 or character == 13:   # Handle the return key
				path = os.path.expanduser(self.buffer)
				fd = open(path, "w")
				fd.write(self.editor.buffer)
				fd.close()
				self.buffer = ""
				self.saving = False
				self.editor.active = True
			else:
				try: self.buffer += chr(character)     # Append input to buffer
				except: pass
			line = "Filename: " + self.buffer
			line += ' ' * (self.width - len(line))
			self.change_content(0, line, ALIGN_LEFT, palette(self.col[0], self.col[1]))

	def compute_status_line(self):
		line = ''
		c = len(self.editor.buffer)
		if c:
			line  = "C%i, " % c
		w = len(self.editor.buffer.split())
		if w:
			line += "W%i, " % w
		l = len(self.editor.buffer.split('\n'))
		if l:
			line += "L%i" % l
		filler =  ' ' * ((self.width /2) - (len(line) / 2))
		line = filler + line
		line += ' ' * (self.width-len(line))
		self.change_content(0, line, ALIGN_LEFT, palette(self.col[0], self.col[1]))



if __name__ == "__main__":
	window = Window()
	editor = Editor("editor")
	status = Status("status")
	editor.status = status
	status.editor = editor
	window.add(editor)
	window.add(status)
	window.exit_keys.append(24) # ^X
	try:
		window.start()
	except KeyboardInterrupt:
		pass
