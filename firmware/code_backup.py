import adafruit_matrixkeypad
from digitalio import DigitalInOut
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid
import board
import time

# Classic 3x4 matrix keypad
# We don't actually use key number 9
cols = [DigitalInOut(x) for x in (board.D9, board.D4, board.D3)]
rows = [DigitalInOut(x) for x in (board.D2, board.D1, board.D10)]
keys = ((6, 7, 8),
        (3, 4, 5),
        (1, 2, 9))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

hold_amount = 1.0
hold_time = [0, 0, 0, 0, 0, 0, 0, 0]

# refer to the documentation for a list of available keycodes:
# https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.keycode.Keycode
keypress_map = {
    1: lambda: layout.write("Hello, World!"),  # type a sequence of letters
    2: lambda: kbd.send(Keycode.A),  # type a single character
    3: lambda: kbd.send(Keycode.B),  # copy and paste
    4: lambda: kbd.send(Keycode.C),  # by sending multiple keycodes
    5: lambda: kbd.send(Keycode.D),  # change these to suit your needs!
    6: lambda: kbd.send(Keycode.E),
    7: lambda: kbd.send(Keycode.F),
    8: lambda: kbd.send(Keycode.G),
}

while True:
    for k in [1, 2, 3, 4, 5, 6, 7, 8]:
        if k in keypad.pressed_keys:
            if hold_time[k-1] == 0:
                keypress_map[k]()
                hold_time[k-1] += 0.05
            elif hold_time[k-1] < hold_amount:
                hold_time[k-1] += 0.05
            else:
                keypress_map[k]()
        else:  # key not pressed
            hold_time[k-1] = 0
    time.sleep(0.01)
