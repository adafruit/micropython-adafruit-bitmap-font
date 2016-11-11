# CharlieWing message scroller example.
# This is currently written for the SAMD21 MicroPython port, but adjust the I2C
# initialization at the bottom for other ports.
# Author: Tony DiCola
# License: Public Domain
import bitmapfont
import is31fl3731
import machine
import utime


# Configuration:
MESSAGE        = 'MicroPython rocks!'
DISPLAY_WIDTH  = 15    # Display width in pixels.
DISPLAY_HEIGHT = 7     # Display height in pixels.
INTENSITY      = 255   # Message pixel brightness (0-255).
SPEED          = 25.0  # Scroll speed in pixels per second.


def main(i2c):
    # Initialize Charlieplex matrix wing.
    matrix = is31fl3731.CharlieWing(i2c)
    matrix.fill(0)
    # Initialize font renderer.
    with bitmapfont.BitmapFont(DISPLAY_WIDTH, DISPLAY_HEIGHT, matrix.pixel) as bf:
        # Global state:
        pos = DISPLAY_WIDTH                 # X position of the message start.
        message_width = bf.width(MESSAGE)   # Message width in pixels.
        frame = 0                           # Currently displayed frame.
        last = utime.ticks_ms()             # Last frame millisecond tick time.
        speed_ms = SPEED / 1000.0           # Scroll speed in pixels/ms.
        while True:
            # Compute the time delta in milliseconds since the last frame.
            current = utime.ticks_ms()
            delta_ms = utime.ticks_diff(last, current)
            last = current
            # Compute position using speed and time delta.
            pos -= speed_ms*delta_ms
            if pos < -message_width:
                pos = DISPLAY_WIDTH
            # Swap frames to start drawing on a non-visible frame (double buffering).
            frame = (frame + 1) % 2
            matrix.frame(frame, show=False)
            # Clear the frame and draw the text at the current position.
            matrix.fill(0)
            bf.text(MESSAGE, int(pos), 0, INTENSITY)
            # Swap to the new frame on the display.
            matrix.frame(frame)
            # Sleep a bit to give USB mass storage some processing time (quirk
            # of SAMD21 firmware right now).
            utime.sleep_ms(20)


with machine.I2C(machine.Pin('SCL'), machine.Pin('SDA')) as i2c:
    main(i2c)
