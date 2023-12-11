import adafruit_matrixkeypad
from digitalio import DigitalInOut
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import usb_hid
#import adafruit_rgbled
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

cc = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

hold_amount = 1.0
hold_time = [[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0]]

# refer to the documentation for a list of available keycodes:
# https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.keycode.Keycode
keypress_map = {
    # STANDARD KEYS
    (0, 1): lambda: cc.send(ConsumerControlCode.VOLUME_DECREMENT),	# volume up
    (0, 2): lambda: cc.send(ConsumerControlCode.VOLUME_INCREMENT),	# volume down
    (0, 3): lambda: None, # N/A (modifier 1)				# N/A
    (0, 4): lambda: kbd.send(Keycode.CONTROL, Keycode.X),		# cut
    (0, 5): lambda: cc.send(ConsumerControlCode.PLAY_PAUSE),		# play/pause
    (0, 6): lambda: None, # N/A (modifier 1),				# N/A
    (0, 7): lambda: kbd.send(Keycode.CONTROL, Keycode.C),		# copy
    (0, 8): lambda: kbd.send(Keycode.CONTROL, Keycode.V),		# paste
    # MODIFIER 1
    (1, 1): lambda: kbd.send(Keycode.CONTROL, Keycode.KEYPAD_NINE),	# tab left
    (1, 2): lambda: kbd.send(Keycode.CONTROL, Keycode.KEYPAD_THREE),	# tab right
    (1, 3): lambda: layout.write("L3"),					# N/A
    (1, 4): lambda: kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.KEYPAD_FOUR),	# highlight left
    (1, 5): lambda: kbd.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.KEYPAD_SIX),	# highlight right
    (1, 6): lambda: layout.write("L6"),					# N/A
    (1, 7): lambda: kbd.send(Keycode.CONTROL, Keycode.C),		# copy
    (1, 8): lambda: kbd.send(Keycode.CONTROL, Keycode.V),		# paste
    # MODIFIER 2
    (2, 1): lambda: layout.write("R1"),
    (2, 2): lambda: layout.write("R2"),
    (2, 3): lambda: layout.write("R3"),
    (2, 4): lambda: layout.write("R4"),
    (2, 5): lambda: layout.write("R5"),
    (2, 6): lambda: layout.write("R6"),
    (2, 7): lambda: layout.write("R7"),
    (2, 8): lambda: layout.write("R8"),
    # BOTH MODIFIERS
    (3, 1): lambda: layout.write("B1"),
    (3, 2): lambda: layout.write("B2"),
    (3, 3): lambda: layout.write("B3"),
    (3, 4): lambda: layout.write("B4"),
    (3, 5): lambda: layout.write("B5"),
    (3, 6): lambda: layout.write("B6"),
    (3, 7): lambda: layout.write("B7"),
    (3, 8): lambda: layout.write("B8")
}

while True:
    # setting up shifter
    shift = 0
    special = {3, 6}
    for n in special:  ### mutated ###
        if n in keypad.pressed_keys: shift+=n
    shift //= 3

    for k in {1, 2, 3, 4, 5, 6, 7, 8}-special:
        if k in keypad.pressed_keys:
            if hold_time[shift][k] == 0:
                keypress_map[(shift, k)]()
                hold_time[shift][k] += 0.05
            elif hold_time[shift][k] < hold_amount:
                hold_time[shift][k] += 0.05
            else:
                keypress_map[(shift, k)]()
        else:  # key not pressed
            hold_time[shift][k] = 0
    time.sleep(0.01)
