# CircuitPython IO demo #1 - General Purpose I/O
import time
import board
import busio

from digitalio import DigitalInOut, Direction, Pull


# Import the HT16K33 LED segment module.
from adafruit_ht16k33 import segments

from adafruit_debouncer import Debouncer

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)


class CountdownTimer(object):
    """Countdown timer for a chess player.

    Parameters
    ----------
    time_left : `integer`
       Time remaining on the clock, initial value is game length.
    display : `Seg7x4`
       Adafruit LED display object.
    display : `switch`
       Button object to pause timer.
    display : `active`
       Flag to identify if clock is active and counting down.
    display : `increment`
       Time to add to clock after a pause (making a move).
    """

    def __init__(self, time_left, display, pin, active=False, increment=0):
        self.increment = increment
        self.time_left = time_left
        self.time_start = time.monotonic()
        self.display = display
        self.active = active
        self.pin = pin
        self.pin.direction = Direction.INPUT
        self.pin.pull = Pull.UP
        self.switch = Debouncer(pin)
        self.get_display(self.time_left)
        self.display.show()
        self.started = False
        self.flagged = False

    def get_display(self, time_left):
        """Recieve seconds left on the clock and return formatted output.
        """
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
        """Calculate time remaining on countdown and send to display.

        Always running this function will display a real time countdown.
        """
        time_now = time.monotonic()
        delta = time_now - (self.time_start)
        self.time_left = self.time_left - delta
        self.time_start = time_now
        return self.get_display(self.time_left)

    def run_clock(self):
        """Run the countdown and listen for pauses.
        """
        while (self.time_left > 0) and (self.active):
            self.switch.update()
            if self.switch.fell:
                self.pause()
            time_display = self.get_time_remaining()
        if self.time_left <= 0:
            self.flagged = True

    def start(self):
        """Start the countdown timer.
        """
        time_now = time.monotonic()
        self.time_start = time_now
        self.started = True

    def pause(self):
        """Pause the countdown timer.
        """
        self.active = False
        self.time_left = self.time_left + self.increment

    def resume(self):
        """Resume the countdown timer.
        """
        self.time_start = time.monotonic()
        self.active = True
        self.run_clock()


def main():
    s = CountdownTimer(time_left = 66, display = segments.Seg7x4(i2c), pin = DigitalInOut(board.D5), active = False, increment=5)
    b = CountdownTimer(time_left = 66, display = segments.Seg7x4(i2c, address=0x71), pin = DigitalInOut(board.D6), active = False, increment=5)

    while s.active == False:
        b.switch.update()
        if b.switch.fell:
            s.active = True

    while True:
        while s.active and (s.flagged == False):
            if s.started == False:
                s.start()
                s.run_clock()
            else:
                s.resume()
            if s.switch.fell:
                s.active = False
                b.active = True

        while b.active and (b.flagged == False):
            if b.started == False:
                b.start()
                b.run_clock()
            else:
                b.resume()
            if b.switch.fell:
                b.active = False
                s.active = True

if __name__ == "__main__":
    main()
