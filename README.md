# Chess Clock

chess-clock is a circuitpython library for creating and controlling a chess clock.

This library handles both the software and hardware implementation.

Designed for circuitpython 5.0.X

## Installation

Clone the repository.

If your hardware needs the memory optimized it is recommended to convert ```timer.py``` and ```chessclock.py``` to *.mpy* files. [Seen here.](https://learn.adafruit.com/adafruit-feather-m0-express-designed-for-circuit-python-circuitpython/frequently-asked-questions#how-can-i-create-my-own-mpy-files-3-11)

Copy ```code.py```,```timer.(m)py``` and ```chessclock.(m)py``` to your circuitpython device.

## Hardware Overview

1 x [Featherboard M0 w/ circuitpython](https://www.adafruit.com/product/3403)

2 x [7-segment display](https://www.adafruit.com/product/3109) Be sure to set up unique addresses ([guide](https://learn.adafruit.com/adafruit-led-backpack/changing-i2c-address#changing-addresses-50-1))

2 x Buttons

1 x [Lithium Ion Polymer Battery](https://www.adafruit.com/product/2750) (recommended)

1 x Power/Reset Button (optional)


## Usage

Configure your clock as desired in `code.py`.

```python

player_1 = chessclock.ChessClock(time_left = 60,
                                 display = segments.Seg7x4(i2c),
                                 pin = DigitalInOut(board.D5),
                                 increment = 5)

player_2 = chessclock.ChessClock(time_left = 60,
                                 display = segments.Seg7x4(i2c, address=0x71),
                                 pin = DigitalInOut(board.D6),
                                 increment=5)

```

Clock will start after a button is pressed. When the active player presses their button, their timer will pause and the other player's timer will start.

## Contributing
Pull requests are always welcome. For major changes, please open an issue first to discuss what you would like to change.

Fork > Clone Fork > Branch Clone > Make Changes > Commit Branch > Pull Request
