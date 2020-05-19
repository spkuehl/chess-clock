# Import the HT16K33 LED segment module.
from adafruit_ht16k33 import segments
from digitalio import DigitalInOut
import board
import busio

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

import chessclock

def main():
    player_1 = chessclock.ChessClock(time_left = 60,
                                     display = segments.Seg7x4(i2c),
                                     pin = DigitalInOut(board.D5), increment=5)

    player_2 = chessclock.ChessClock(time_left = 60,
                                     display = segments.Seg7x4(i2c,
                                                               address=0x71),
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
        #Run this loop during player_1's turn.
        while player_1.active and (player_1.flagged == False):
            if player_1.started == False:
                player_1.start()
                player_1.run_clock()
            else:
                player_1.resume()
                player_1.run_clock()
            if player_1.switch.fell: #Check if player_1 ends their turn.
                player_1.active = False
                player_2.active = True

        #Run this loop during player_2's turn.
        while player_2.active and (player_2.flagged == False):
            if player_2.started == False:
                player_2.start()
                player_2.run_clock()
            else:
                player_2.resume()
                player_2.run_clock()
            if player_2.switch.fell: #Check if player_2 ends their turn.
                player_2.active = False
                player_1.active = True

if __name__ == "__main__":
    main()
