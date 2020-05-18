from adafruit_debouncer import Debouncer
import timer
from digitalio import Direction, Pull


class ChessClock(timer.Timer):
    """Countdown timer for a chess player.

    Parameters
    ----------
    display : `Seg7x4`
       Adafruit LED display object.
    display : `pin`
       Digital Input object to pause timer (the button).
    display : `increment`
       Time to add to clock after a pause (making a move).
    """

    def __init__(self, time_left, display, pin, increment=0):
        timer.Timer.__init__(self, time_left=time_left)
        self.increment = increment
        self.display = display
        #Configure the Debouncer switch.
        self.pin = pin
        self.pin.direction = Direction.INPUT
        self.pin.pull = Pull.UP
        self.switch = Debouncer(pin)
        self.show_display()
        self.display.show()
        self.flagged = False #True indicates time is expired

    def show_display(self):
        """Recieve seconds left on the clock and return formatted output.
        """
        if self.time_left > 60:
            minutes = int(self.time_left) // 60
            seconds = int(self.time_left) % 60
            time_display = (minutes, seconds)
        else:
            seconds = int(self.time_left)
            milliseconds = int((self.time_left-int(self.time_left))*100)
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

    def run_clock(self):
        """Run the countdown and listen for pauses.
        """
        while (self.time_left > 0) and (self.active):
            self.update_time_remaining()
            self.show_display()
            self.switch.update()
            if self.switch.fell:
                self.pause()
                self.time_left = self.time_left + self.increment
                self.show_display()
        if self.time_left <= 0:
            self.flagged = True
