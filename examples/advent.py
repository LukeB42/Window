#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# An adventure game example
import random
from window import Window, Pane, Menu, EXPAND, FIT, ALIGN_LEFT, palette

class Person(object):
    level   = 1
    health  = [100, 100] # [actual, maximum]
    mana    = [100, 100]
    money   = 100
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

    Doubles as a loading bar if used in reverse.
    """
    geometry = [EXPAND, 1]
    def update(self):
        h = self.window.player.health
        if h[0] <= 0:
            self.window.stop()

        amt = int(self.width * float(h[0]) / float(h[1]))
        
        healthbar = "Health: %3.f/%i" % (h[0],h[1]) 
        healthbar += ' ' * (amt - len(healthbar))

        if h[0] < (h[1] / 3):
            colours = palette("black", "red")
        elif h[0] < (h[1] / 2):
            colours = palette("black", "yellow")
        else:
            colours = palette("black", "green")

        self.change_content(0, healthbar, ALIGN_LEFT, colours)
        self.change_content(1, ' ' * (self.width - len(healthbar)), ALIGN_LEFT, palette(-1,-1))

class ManaBar(Pane):
    geometry = [EXPAND, 1]
    def update(self):
        h = self.window.player.mana

        amt = int(self.width * float(h[0]) / float(h[1]))
        
        healthbar = "Mana:   %3.f/%i" % (h[0],h[1]) 
        healthbar += ' ' * (amt - len(healthbar))

        if h[0] < (h[1] / 4):
            colours = palette("black", "yellow")
#        elif h[0] < (h[1] / 2):
#            colours = palette("black", "yellow")
        else:
            colours = palette("black", "blue")

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
        # self.window.player.health[0] -= 1
        pass

class Input(Pane):
    """
    A test pane.
    """
    geometry = [EXPAND, 1]    # horiz, vert
    buffer   = ""

    def update(self):
        new_line = ">"
        self.change_content(0, new_line)
#        if len(self.content) >= 2:
#            self.change_content(2, "%i\n" % len(self.buffer))

    def process_input(self, character):
        self.window.window.clear()
        if character == 263 and self.buffer:     # Handle backspace
            self.buffer = self.buffer[:-1]
        elif character == 10 or character == 13: # Handle the return key
            inputs = self.buffer.split("\n")
            if "menu" in inputs:
                menu = self.window.get("menu")
                menu.hidden = False if menu.hidden else True
                menu.active = True if not menu.active else False
            elif "exit" in inputs:
                self.window.stop()
            self.buffer = ""
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
    geometry = [FIT, FIT]
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

def start_sequence(window, start_window=True):
    print "Hi. What's your name?"
    window.player.name = raw_input("> ")
    print "Hello %s. " % window.player.name,
    classes = ["Magi", "Warrior", "Thief", "Engineer"]
    def choose_class():
        print "What's your class?"
        for i,c in enumerate(classes):
            print "%i: %s" % (i,c)
        selection = raw_input("> ")
        if selection.isdigit():
            return int(selection)
        else:
            choose_class()
    selection = choose_class()
    print selection
    window.player.pclass = PClass(classes[selection])
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

    manabar = ManaBar("manabar")
    window.add(manabar)

    healthbar = HealthBar("healthbar")
    window.add(healthbar)

    input_pane = Input("input")
    input_pane.active = True
    menu = TestMenu("menu")
    window.add([menu, input_pane])
    menu.active = False
    menu.hidden = True
    window.exit_keys.append(4) # ^D to exit

    # ask for player info:
    try:
        start_sequence(window)
    except KeyboardInterrupt:
        window.stop()
        print "^C"
        raise SystemExit
