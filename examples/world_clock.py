#!/usr/bin/env python2
# _*_ coding: utf-8 _*_
# Implements an ncurses world clock that updates every minute
# To grab the 3rd party libraries: sudo pip install pytz window
import pytz
import time
import window
from datetime import datetime

times = """
America/New_York
Europe/London
Europe/Berlin
Asia/Tel_Aviv
Asia/Dubai
Asia/Shanghai
Asia/Tokyo
"""

class WorldClock(window.Pane):
    geometry = [window.EXPAND, window.EXPAND]
    def update(self):
        self.change_content(0, "", window.ALIGN_LEFT, window.palette(-1,-1))
        for i, timezone in enumerate(times.split('\n')):
            if not timezone: continue
            # We can append the text to the zeroth content frame using the
            # additive assignment operator. Specifying which frame to append to
            # is done with an int as the first element in a tuple:
            # self += (1, "This is concatenated on to the second content frame.")
            tz = pytz.timezone(timezone)
            self += datetime.now(tz).strftime(timezone + "\t%H:%M")
            if not i % 2:
                self += '\n'
            else:
                self += ' '

if __name__ == "__main__":
    win         = window.Window(blocking=False)
    win.delay   = 60
    world_clock = WorldClock("world_clock")
    win.add(world_clock)
    win.exit_keys.append(4) # ^D to exit
    try:
        win.start()
    except KeyboardInterrupt:
        win.stop()
