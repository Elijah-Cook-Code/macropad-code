import board
import keypad
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import usb_hid
import rotaryio
import digitalio
import busio
import lcd
import i2c_pcf8574_interface
import random

# Define modes
MODE_BLENDER = 0
MODE_KRITA = 1
MODE_DICE = 2

# Initialize current mode
current_mode = MODE_BLENDER

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices) 

# Create KeyMatrix to read key presses
matrix = keypad.KeyMatrix(
    row_pins=(board.GP10, board.GP11, board.GP12, board.GP13),
    column_pins=(board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9)
)

# Set up I2C for LCD
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
address = 0x27
i2c = i2c_pcf8574_interface.I2CPCF8574Interface(i2c, address)

# Set up LCD display
display = lcd.LCD(i2c, num_rows=2, num_cols=16)
display.set_backlight(True)
display.set_display_enabled(True)
display.clear()

# Initialize rotary encoder
encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP18)
switch = digitalio.DigitalInOut(board.GP19)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Initialize rotary encoder for mode selection
encoder_mode = rotaryio.IncrementalEncoder(board.GP22, board.GP21)
switch_mode = digitalio.DigitalInOut(board.GP20)
switch_mode.direction = digitalio.Direction.INPUT
switch_mode.pull = digitalio.Pull.UP

# Adjustable thresholds for volume control
VOLUME_STATE = 0
VOLUME_THRESHOLD = 2

# Debounce delay in seconds
DEBOUNCE_DELAY_KEYPAD = 0.1
DEBOUNCE_DELAY_ENCODER = 0.1

# Initialize last switch state for debounce
switch_last_state = switch.value
switch_last_time = time.monotonic()

def roll_dice(sides):
    """Simulate rolling a dice with a given number of sides."""
    return random.randint(1, sides)

def keypad_input():
    try:
        event = matrix.events.get()
        if event:
            key_number = event.key_number
            if event.pressed:
                print(f'Key pressed: {key_number}')
                # Perform action based on key number
                handle_key_press(key_number)
            else:
                print(f'Key released: {key_number}')
                kbd.release_all()
                
    except Exception as e:
        print("An error in keypad_input occurred: {}".format(e))
        
def volume_control(position):
    global VOLUME_STATE
    global VOLUME_THRESHOLD

    delta = position - VOLUME_STATE

    if abs(delta) >= VOLUME_THRESHOLD:
        if delta > 0:
            VOLUME_STATE = position
            print("Volume Up")
            for _ in range(abs(delta)):
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                time.sleep(0.1)
        elif delta < 0:
            VOLUME_STATE = position
            print("Volume Down")
            for _ in range(abs(delta)):
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                time.sleep(0.1)

def play_pause():
    global switch_last_state
    global switch_last_time

    switch_state = switch.value

    if switch_state != switch_last_state:
        switch_last_time = time.monotonic()

    if time.monotonic() - switch_last_time > DEBOUNCE_DELAY_ENCODER:
        if not switch_state:
            cc.send(ConsumerControlCode.PLAY_PAUSE)
            time.sleep(0.1)

    switch_last_state = switch_state
    
def handle_key_press(key_number):
    global current_mode

    if current_mode == MODE_DICE:
        if key_number == 0:
            result = roll_dice(4)
            display.clear()
            display.print(f"Rolled d4: {result}")
            print(f"Rolled d4: {result}")
        elif key_number == 1:
            result = roll_dice(6)
            display.clear()
            display.print(f"Rolled d6: {result}")
            print(f"Rolled d6: {result}")
        elif key_number == 2:
            result = roll_dice(8)
            display.clear()
            display.print(f"Rolled d8: {result}")
            print(f"Rolled d8: {result}")
        elif key_number == 3:
            result = roll_dice(10)
            display.clear()
            display.print(f"Rolled d10: {result}")
            print(f"Rolled d10: {result}")
        elif key_number == 4:
            result = roll_dice(12)
            display.clear()
            display.print(f"Rolled d12: {result}")
            print(f"Rolled d12: {result}")
        elif key_number == 5:
            result = roll_dice(20)
            display.clear()
            display.print(f"Rolled d20: {result}")
            print(f"Rolled d20: {result}")
    
    elif current_mode == MODE_BLENDER:
        if key_number == 0:
            print("Typing 'tab'")
            kbd.press(Keycode.TAB)
        elif key_number == 1:
            print("Typing 'B'")
            kbd.press(Keycode.B)
        elif key_number == 2:
            print("Typing 'G'")
            kbd.press(Keycode.G)
        elif key_number == 3:
            print("Typing 'R'")
            kbd.press(Keycode.R)
        elif key_number == 4:
            print("Typing 'S'")
            kbd.press(Keycode.S)
        elif key_number == 5:
            print("Typing 'O'")
            kbd.press(Keycode.O)
        elif key_number == 6:
            print("Typing 'E'")
            kbd.press(Keycode.E)
        elif key_number == 7:
            print("Typing 'I'")
            kbd.press(Keycode.I)
        elif key_number == 8:
            print("Typing 'X'")
            kbd.press(Keycode.X)
        elif key_number == 9:
            print("Typing 'Y'")
            kbd.press(Keycode.Y)
        elif key_number == 10:
            print("Typing 'Z'")
            kbd.press(Keycode.Z)
        elif key_number == 11:
            print("Typing 'undo'")
            kbd.press(Keycode.CONTROL, Keycode.Z)
        elif key_number == 12:
            print("Typing 'ZERO'")
            kbd.press(Keycode.KEYPAD_ZERO)
        elif key_number == 13:
            print("Typing 'NUM .'")
            kbd.press(Keycode.KEYPAD_PERIOD)
        elif key_number == 14:
            print("Typing '1'")
            kbd.press(Keycode.ONE)
        elif key_number == 15:
            print("Typing '2'")
            kbd.press(Keycode.TWO)
        elif key_number == 16:
            print("Typing '3'")
            kbd.press(Keycode.THREE)
        elif key_number == 17:
            print("Typing 'CRTL + Z'")
            kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.Z)
        elif key_number == 18:
            print("Typing 'shift'")
            kbd.press(Keycode.SHIFT)
        elif key_number == 19:
            print("Typing 'SHIFT + ALT'")
            kbd.press(Keycode.SHIFT, Keycode.ALT)
        elif key_number == 20:
            print("Typing 'A'")
            kbd.press(Keycode.A)
        elif key_number == 21:
            print("Typing 'SHIFT + A'")
            kbd.press(Keycode.SHIFT, Keycode.A)
        elif key_number == 22:
            print("Typing 'loop cut'")
            kbd.press(Keycode.CONTROL, Keycode.R)
        elif key_number == 23:
            print("Typing 'CRTL + SAVE'")
            kbd.press(Keycode.CONTROL, Keycode.S)

    elif current_mode == MODE_KRITA:
        if key_number == 0:
            print("Typing 'tab'")
            kbd.press(Keycode.TAB)
        elif key_number == 1:
            print("Typing 'B'")
            kbd.press(Keycode.B)
        elif key_number == 2:
            print("Typing 'G'")
            kbd.press(Keycode.CONTROL, Keycode.T)
        elif key_number == 3:
            print("Typing 'R'")
            kbd.press(Keycode.CONTROL, Keycode.A)
        elif key_number == 4:
            print("Typing 'S'")
            kbd.press(Keycode.CONTROL, Keycode.J)
        elif key_number == 5:
            print("Typing 'O'")
            kbd.press(Keycode.CONTROL, Keycode.O)
        elif key_number == 6:
            print("Typing 'E'")
            kbd.press(Keycode.CONTROL, Keycode.E)
        elif key_number == 7:
            print("Typing 'I'")
            kbd.press(Keycode.CONTROL, Keycode.I)
        elif key_number == 8:
            print("Typing 'X'")
            kbd.press(Keycode.CONTROL, Keycode.X)
        elif key_number == 9:
            print("Typing 'Y'")
            kbd.press(Keycode.CONTROL, Keycode.Y)
        elif key_number == 10:
            print("Typing 'Z'")
            kbd.press(Keycode.CONTROL, Keycode.Z)
        elif key_number == 11:
            print("Typing 'undo'")
            kbd.press(Keycode.CONTROL, Keycode.Z)
        elif key_number == 12:
            print("Typing 'ZERO'")
            kbd.press(Keycode.KEYPAD_ZERO)
        elif key_number == 13:
            print("Typing 'NUM .'")
            kbd.press(Keycode.KEYPAD_PERIOD)
        elif key_number == 14:
            print("Typing '1'")
            kbd.press(Keycode.ONE)
        elif key_number == 15:
            print("Typing '2'")
            kbd.press(Keycode.TWO)
        elif key_number == 16:
            print("Typing '3'")
            kbd.press(Keycode.THREE)
        elif key_number == 17:
            print("Typing 'CRTL + Z'")
            kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.Z)
        elif key_number == 18:
            print("Typing 'shift'")
            kbd.press(Keycode.SHIFT)
        elif key_number == 19:
            print("Typing 'SHIFT + ALT'")
            kbd.press(Keycode.SHIFT, Keycode.ALT)
        elif key_number == 20:
            print("Typing 'A'")
            kbd.press(Keycode.A)
        elif key_number == 21:
            print("Typing 'SHIFT + A'")
            kbd.press(Keycode.SHIFT, Keycode.A)
        elif key_number == 22:
            print("Typing 'loop cut'")
            kbd.press(Keycode.CONTROL, Keycode.R)
        elif key_number == 23:
            print("Typing 'CRTL + SAVE'")
            kbd.press(Keycode.CONTROL, Keycode.S)

def update_mode():
    global current_mode

    mode_position = encoder_mode.position
    if mode_position % 3 == 0:
        current_mode = MODE_BLENDER
        display.clear()
        display.print("Mode: Blender")
        print("Switched to Blender Mode")
    elif mode_position % 3 == 1:
        current_mode = MODE_KRITA
        display.clear()
        display.print("Mode: Krita")
        print("Switched to Krita Mode")
    elif mode_position % 3 == 2:
        current_mode = MODE_DICE
        display.clear()
        display.print("Mode: Dice")
        print("Switched to Dice Mode")

while True:
    try:
        update_mode()
        keypad_input()
        volume_control(encoder.position)
        play_pause()
        
    except Exception as e:
        print(f"An error occurred: {e}")
