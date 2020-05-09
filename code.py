# CircuitPython IO demo #1 - General Purpose I/O
import time
import board
import busio

from digitalio import DigitalInOut, Direction, Pull

import rtc
import time


# Import the HT16K33 LED segment module.
from adafruit_ht16k33 import segments

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)



class CountdownTimer(object):
    def __init__(self, time_left, display, switch, active=False, increment=0):
        self.increment = increment
        self.time_left = time_left
        self.time_start = time.monotonic()
        self.display = display
        self.active = active
        self.switch = switch
        self.switch.direction = Direction.INPUT
        self.switch.pull = Pull.UP
        self.get_display(self.time_left)
        self.display.show()
        self.started = False
        self.flagged = False

    def get_display(self, time_left):
        if time_left > 60:
            minutes = int(time_left) // 60
            seconds = int(time_left) % 60
            time_display = (minutes, seconds)
        else:
            seconds = int(time_left)
            milliseconds = int((time_left-int(time_left))*100)
            time_display = (seconds, milliseconds)

        if int(self.time_left)%2 == 0:
            self.display.colon = True
        else:
            self.display.colon = False

        if time_display[0] >= 10:
            self.display[0] = str(time_display[0])[0]
            self.display[1] = str(time_display[0])[1]
        else:
            self.display[0] = ' '
            self.display[1] = str(time_display[0])[0]

        if time_display[1] >= 10:
            self.display[2] = str(time_display[1])[0]
            self.display[3] = str(time_display[1])[1]
        else:
            self.display[2] = '0'
            self.display[3] = str(time_display[1])[0]

        self.display.show()

    def get_time_remaining(self):
        time_now = time.monotonic()
        delta = time_now - (self.time_start)
        self.time_left = self.time_left - delta
        self.time_start = time_now
        return self.get_display(self.time_left)

    def run_clock(self):
        while (self.time_left > 0) and (self.active):
            if self.switch.value:
                pass
            else:
                self.pause()
            time_display = self.get_time_remaining()
        if self.time_left == 0:
            self.flagged = True

    def start(self):
        time_now = time.monotonic()
        self.time_start = time_now
        self.started = True

    def pause(self):
        self.active = False
        self.time_left = self.time_left + self.increment

    def resume(self):
        self.time_start = time.monotonic()
        self.active = True
        self.run_clock()


s = CountdownTimer(time_left = 66, display = segments.Seg7x4(i2c, auto_write=False), switch = DigitalInOut(board.D5), active = False, increment=5)
b = CountdownTimer(time_left = 66, display = segments.Seg7x4(i2c, address=0x71), switch = DigitalInOut(board.D6), active = False, increment=5)

while s.active == False:
    if b.switch.value:
        pass
    else:
        b.active = False
        s.active = True

while True:
    while s.active and (s.flagged == False):
        if s.started == False:
            s.start()
            s.run_clock()
        else:
            s.resume()
        if s.switch.value:
            pass
        else:
            s.active = False
            b.active = True

    while b.active and (b.flagged == False):
        if b.started == False:
            b.start()
            b.run_clock()
        else:
            b.resume()
        if b.switch.value:
            pass
        else:
            b.active = False
            s.active = True
