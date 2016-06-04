#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import window
import requests
import goose
import random
import string

class CornerPane(window.Pane):
    geometry          = [10, 10]
    self_coordinating = True
    def update(self):
        updatestr = ""
        for _ in range(50):
            updatestr += random.choice(string.ascii_letters)
            updatestr += '\n' * random.randint(0, 5)
        self.change_content(0, updatestr)
        self.coords[0] = ((random.randint(0,10), random.randint(0,10)), (random.randint(0,10), random.randint(0,10)))
        self.coords[1] = ((random.randint(0,10), random.randint(0,10)), (random.randint(0,10), random.randint(0,10)))

if __name__ == "__main__":
    win = window.Window(blocking=True)
    win.debug = True
    win.delay = 1
    a = CornerPane(str(random.randint(100,999)))
    b = CornerPane(str(random.randint(100,999)))
    c = CornerPane(str(random.randint(100,999)))
    d = CornerPane(str(random.randint(100,999)))
    
    win.add([a,b,c,d])
    try:
        win.start()
    except KeyboardInterrupt:
        win.stop()
