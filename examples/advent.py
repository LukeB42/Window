#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# An adventure game example
import random
from window import Window, Pane, Menu, EXPAND, FIT, ALIGN_LEFT, palette

class Person(object):
	level = 1
	health = [100, 100] # [actual, maximum]
	mana = 100
	money = 100
	weapons = None
	weapons = []

class Player(Person):
	pass

class PClass(object):
	def __init__(self, name):
		self.class_type = name

class NPC(Person):
	friendlyness = 10

class Location(object):
	name = ""
	description = ""

class Weapon(object):
	name = ""
	description = ""
	power = 0
	def __init__(self, name):
		self.name = name

class CombatMenu(Menu):
	"""
	Menu navigation for combat
	"""
	geometry = [EXPAND, EXPAND]

class HealthBar(Pane):
	"""
	Player condition (health, mana, attr)
	"""
	geometry = [EXPAND, 1]
	def update(self):
		h = self.window.player.health
		if h[0] <= 0:
			self.window.stop()

		amt = int(self.width * float(h[0]) / float(h[1]))
		
		healthbar = "Health: %i/%i" % (h[0],h[1]) 
		healthbar += ' ' * (amt - len(healthbar))

		if h[0] < (h[1] / 3):
			colours = palette("black", "yellow")
		elif h[0] < (h[1] / 2):
			colours = palette("black", "red")
		else:
			colours = palette("black", "green")

		self.change_content(0, healthbar, ALIGN_LEFT, colours)
		self.change_content(1, ' ' * (self.width - len(healthbar)), ALIGN_LEFT, palette(-1,-1))

class GameArea(Pane):
	"""
	The main area where events are written to.
	"""
	geometry = [EXPAND, EXPAND]

	def update(self):
		self.change_content(0, "You are likely to be eaten by a grue.", ALIGN_LEFT, palette("red"))

	def process_input(self, character):
		self.window.player.health[0] -= 1

class Input(Pane):
	"""
	An input area for typing commands
	Essentially contains the core game logic.

	"""
	geometry = [EXPAND, EXPAND]

	def process_input(self, character):
		self.window.stop()

def start_sequence(window, start_window=True):
	print "Hello there, what is your name?"
	window.player.name = raw_input("> ")
	print "Hello %s. What is your class?" % window.player.name
	window.player.pclass = PClass(raw_input("> "))
	print "Cool. A %s. Choose your weapon!" % window.player.pclass.class_type
	window.player.weapons.append(Weapon(raw_input("> ")))

	if start_window:
		window.start()

	print "You retired from your adventure at level %i." % window.player.level

if __name__ == "__main__":
	window = Window()

	gamearea = GameArea("gamearea")
	window.add(gamearea)

	window.player = Player()

	healthbar = HealthBar("healthbar")
	window.add(healthbar)

	window.exit_keys.append(4) # ^D to exit

	# ask for player info:
	start_sequence(window)

