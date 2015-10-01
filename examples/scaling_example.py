#!/usr/bin/env python
from window import *

class TestPane(Pane):
	"""
	A test pane.
	"""
	geometry = [EXPAND, EXPAND] # horiz, vert
#	geometry = [EXPAND, FIT]    # horiz, vert
	buffer   = ""

	def update(self):
		import hashlib, random
		if self.name == "test pane 1":
			new_line = 'Scaling example.\n^D or ^Q to exit.\n'
		else:
			new_line = hashlib.sha1(str(random.randint(0,9))).hexdigest() + '\n'
		new_line += "h: %i w: %i\n" % (self.height, self.width)
		self.change_content(0, new_line)
		if len(self.content) >= 2:
			self.change_content(2, "%i\n" % len(self.buffer))
			self.change_content(3, "%s\n" % str(self.coords))

	def process_input(self, character):
		self.window.window.clear()
		if character == 263 and self.buffer:     # Handle backspace
			self.buffer = self.buffer[:-1]
		elif character == 10 or character == 13: # Handle the return key
			self.buffer += "\n"
		else:
			try: self.buffer += chr(character)   # Append input to buffer
			except: pass
		import random
		colours = palette(-1, random.choice(["blue","red"]))
		self.change_content(1, self.buffer, ALIGN_LEFT, colours)

class TestMenu(Menu):
	"""
	An example menu
	"""
	geometry = [FIT, EXPAND]
	items = [
	          [1, 'Hello,','handle_hello'],      # [selected, text, function]
	          [0, 'world','handle_world'],
	          [0, 'fight','handle_fight'],
	          [0, 'items','handle_items'],
	          [0, 'magic','handle_magic'],
	          [0, 'flee','handle_flee'],
	]

	def handle_hello(self):
		phrase = "Hello."
		self.window.addstr(self.window.height-1,
			self.window.width - len(phrase), phrase)

	def handle_world(self):
		phrase = "World."
		self.window.addstr(self.window.height-1,
			self.window.width - len(phrase), phrase)

	def handle_fight(self):
		if self.window.blocking:
			self.window.blocking = False
			self.window.window.nodelay(1)
		else:
			self.window.blocking = True
			self.window.window.nodelay(0)

	def handle_items(self):
		for p in reversed(self.window.panes):
			if isinstance(p, list):
				p.reverse()
				break

	def handle_magic(self):
		if self.geometry[0] == EXPAND:
			self.geometry[0] = FIT
		if self.geometry[0] == FIT:
			self.geometry[0] = 30
		else:
			self.geometry[0] = EXPAND

	def handle_flee(self):
		self.window.stop()

class Status(Pane):
	geometry = [EXPAND, 1]

	def update(self):
		self.change_content(0, "H: %i, W: %i, " % (self.height, self.width))
		self.change_content(1, "C: %s" % str(self.coords))
#		self.quit_for_debugging()

	def quit_for_debugging(self):
		self.window.stop()
		print self.window.height % 2
		print self.window.height
		print pane1.height
		print pane1.coords
		print self.coords

if __name__ == "__main__":
	window = Window(True)
	window.debug = 0
	pane1 = TestPane("test pane 1")
	pane2 = TestPane("test pane 2")

	window.add(pane1)
#	window.add(pane2)

	# Place panes on the horizontal axis by
	# making sublists of panes in window.panes
	pane3 = Editor("test pane 3")
	pane3.wrap = 1
	pane4 = TestPane("test pane 4")
	pane5 = TestPane("test pane 5")

	panes = [pane3,pane4,pane5]
	window.add(panes)

	pane6 = TestPane("test pane 6")
	pane7 = TestMenu("test pane 7")
	panes2 = [pane6,pane7]
	window.add(panes2)

	pane8 = Status("test pane 8")
	window.add(pane8)

#	pane9 = TestPane("test pane 9")
#	window.add(pane9)

	window.exit_keys.append(17) # ^Q to quit
	window.exit_keys.append(4)  # ^D to quit
	try:
		window.start()
	except KeyboardInterrupt:
		window.stop()
	except Exception, e:
		window.stop()
		print e.message

