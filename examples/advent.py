#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# An adventure game example
import sys
import random
from window import Window, Pane, Menu, EXPAND, FIT, ALIGN_LEFT, palette


if sys.version_info.major == 2:
    get_input = raw_input
else:
    get_input = input

class Person(object):
    """
    """
    def __init__(self):
        self.level   = 1
        self.health  = [100, 100] # [actual, maximum]
        self.mana    = [100, 100]
        self.money   = 100
        self.weapons = None
        self.weapons = []

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
        self.change_content(1, ' ' * int(self.width - len(healthbar)), ALIGN_LEFT, palette(-1,-1))

class ManaBar(Pane):
    geometry = [EXPAND, 1]
    def update(self):
        h = self.window.player.mana

        amt = int(self.width * float(h[0]) / float(h[1]))
        
        healthbar = "Mana: %3.f/%i" % (h[0],h[1]) 
        healthbar += ' ' * (amt - len(healthbar))

        if h[0] < (h[1] / 4):
            colours = palette("black", "yellow")
#        elif h[0] < (h[1] / 2):
#            colours = palette("black", "yellow")
        else:
            colours = palette("black", "blue")

        self.change_content(0, healthbar, ALIGN_LEFT, colours)
        self.change_content(1, ' ' * int(self.width - len(healthbar)), ALIGN_LEFT, palette(-1,-1))


class GameArea(Pane):
    """
    The main area where events are written to.
    """
    geometry = [EXPAND, EXPAND]
    intro = """Light, Cytoplasm, RNA messenger molecules,
Intention, Abstraction, Message Integrity, Omnidirectional Infinity

You find yourself manifesting onwards from beyond all spheres of force and matter.

A definite spacetime condenses into view.


You're perceptually drifting along the starboard side of a marchant frigate.

The frigate is heading for the orbit of a nearby planet.


You feel the articulation of suit thrusters guiding you on autopilot alongside
the frigate.

Somewhere in your heart a Mandelbrot set zooms in and out simultaneously.

Solve articulation with the passive neural interface to latch on at an airlock.
"""

    outro = """
You think the required forms to shift through a thin veil of dust, towards
the body of the frigate. The onboard guidance computer flies by wire to a
maintenence station.

<YOU ARE NOT A DROID>

A signal convulses either you, the suit, or the entire yousuit assembly into taking heed

The drone on your back detaches and having been assaying the signals coming from
the frigate the whole time, begins performing aikido in terms of the authentication
protocol used for accessing a maintenence tunnel.

The drone is not a smooth talker. The frigate thinks of you as a hostile parasite.
"""
    def update(self):
        if not self.content:
            self.change_content(0, self.intro, ALIGN_LEFT, palette(-1,-1))

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
        new_line = "> "
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
            # Yup... Can launch ptpython with the "python" command.
            elif "python" in inputs:
                try:
                    from ptpython.repl import embed
                    self.window.stop()
                    l = {"pane": self, "window": self.window}
                    embed(locals=l, vi_mode=True)
                    self.buffer = ""
                    self.window.start()
                except:
                    pass
            elif "exit" in inputs:
                self.window.stop()
            self.buffer = ""
        else:
            try: self.buffer += chr(character)   # Append input to buffer
            except: pass
        import random
        colours = palette(-1, random.choice(["yellow","red"]))
        self.change_content(1, self.buffer, ALIGN_LEFT, colours)

class TestMenu(Menu):
    """
    An example menu
    """
    geometry = [FIT, FIT]
    items = [
              [1, 'fight','handle_fight'],
              [0, 'items','handle_items'],
              [0, 'magic','handle_magic'],
              [0, 'flee','handle_flee'],
    ]

    def handle_fight(self):
        gamearea = self.window.get("gamearea")
        gamearea.change_content(0, "The Grue dissolved.", ALIGN_LEFT, palette(-1,-1))

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
    print("Hi. What's your name?")
    window.player.name = get_input("> ")
    print("Hello %s." % window.player.name,)
    classes = ["Magi", "Warrior", "Thief", "Engineer"]
    def choose_class():
        print("What's your class?")
        for i,c in enumerate(classes):
            print("%i: %s" % (i, c))
        selection = get_input("> ")
        if selection.isdigit():
            return int(selection)
        else:
            choose_class()
    selection = choose_class()
    print(selection)
    window.player.pclass = PClass(classes[selection])
#    print "Cool. A %s. Choose your weapon!" % window.player.pclass.class_type
#    window.player.weapons.append(Weapon(raw_input("> ")))

    if start_window:
        window.start()

    print("You retired from your adventure at level %i." % window.player.level)

if __name__ == "__main__":
    window = Window()

    gamearea = GameArea("gamearea")
    window.add(gamearea)

    window.player = Player()

    manabar = ManaBar("manabar")
#    manabar.hidden = True

    healthbar = HealthBar("healthbar")
#    healthbar.hidden = True
    window.add([healthbar, manabar])

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
        print("^C")
        raise SystemExit
