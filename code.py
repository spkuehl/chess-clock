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
       Time remaining on the clock in seconds, initial value is game length.
    display : `Seg7x4`
       Adafruit LED display object.
    display : `pin`
       Digital Input object to pause timer (the button).
    display : `increment`
       Time to add to clock after a pause (making a move).
    """

    def __init__(self, time_left, display, pin, increment=0):
        self.increment = increment
        self.time_left = time_left
        self.display = display
        self.active = False
        #Configure the Debouncer switch.
        self.pin = pin
        self.pin.direction = Direction.INPUT
        self.pin.pull = Pull.UP
        self.switch = Debouncer(pin)
        self.get_display(self.time_left)
        self.display.show()
        self.started = False
        self.flagged = False #Time is expired

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
    player_1 = CountdownTimer(time_left = 60, display = segments.Seg7x4(i2c),
                              pin = DigitalInOut(board.D5), increment=5)

    player_2 = CountdownTimer(time_left = 60,
                              display = segments.Seg7x4(i2c, address=0x71),
                              pin = DigitalInOut(board.D6), increment=5)


    while player_1.active == False and player_2.active == False:
        #Game starts when a player presses thier timer, opposite clock starts.
        player_1.switch.update()
        if player_1.switch.fell:
            player_2.active = True

        player_2.switch.update()
        if player_2.switch.fell:
            player_1.active = True


    while True:
        while player_1.active and (player_1.flagged == False):
            if player_1.started == False:
                player_1.start()
                player_1.run_clock()
            else:
                player_1.resume()
            if player_1.switch.fell:
                player_1.active = False
                player_2.active = True

        while player_2.active and (player_2.flagged == False):
            if player_2.started == False:
                player_2.start()
                player_2.run_clock()
            else:
                player_2.resume()
            if player_2.switch.fell:
                player_2.active = False
                player_1.active = True


if __name__ == "__main__":
    main()
