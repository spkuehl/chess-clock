import time


class Timer(object):
    """Timer class counting down to zero.

    Parameters
    ----------
    time_left : `integer`
       Time remaining on the clock in seconds, initial value is the duration of
       the timer.
    """

    def __init__(self, time_left):
        self.time_left = time_left
        self.active = False
        self.started = False

    def get_time_remaining(self):
        """Calculate time remaining on countdown.
        """
        if self.active == False:
            return self.time_left
        else:
            time_now = time.monotonic()
            delta = time_now - (self.time_start)
            self.time_left = self.time_left - delta
            self.time_start = time_now
            return self.time_left

    def start(self):
        """Start the countdown timer.
        """
        time_now = time.monotonic()
        self.time_start = time_now
        self.started = True

    def pause(self):
        """Pause the countdown timer.
        """
        time_now = time.monotonic()
        self.time_start = time_now
        self.active = False
        return self.time_left

    def resume(self):
        """Resume the countdown timer.
        """
        self.time_start = time.monotonic()
        self.active = True
        return self.time_left
