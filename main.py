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
import random #for "dnd dice, new mode"

# Define modes
MODE_BLENDER = 0
MODE_KRITA = 1

# Initialize current mode
current_mode = MODE_BLENDER

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices) 

# create KeyMatrix to read key presses
matrix = keypad.KeyMatrix(
    row_pins=(board.GP10, board.GP11, board.GP12, board.GP13),
    column_pins=(board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9 )
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
display.print("NAT 20")

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
VOLUME_THRESHOLD = 2  # Adjust as needed

# Debounce delay in seconds
DEBOUNCE_DELAY_KEYPAD = 0.1  # Adjust as needed
DEBOUNCE_DELAY_ENCODER = 0.1    # Adjust as needed

# Initialize last switch state for debounce
switch_last_state = switch.value
switch_last_time = time.monotonic()

def roll_dice(sides):
    """Simulate rolling a dice with a given number of sides."""
    return random.radint(1, sides)

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
                # Additional logic for key releases can be added here if needed
                kbd.release_all()
                
    except Exception as e:
        print("An error in keypad_input occurred: {}".format(e))
        
def volume_control(position):
    global VOLUME_STATE
    global VOLUME_THRESHOLD

    # Check for a change in position
    delta = position - VOLUME_STATE

    if abs(delta) >= VOLUME_THRESHOLD:
        # Determine the direction of the change
        if delta > 0:
            # Volume up
            VOLUME_STATE = position
            print("Volume Up")
            for _ in range(abs(delta)):
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                time.sleep(0.1)  # Add a small delay between increments
            # Additional logic for volume up can be added here if needed
        elif delta < 0:
            # Volume down
            VOLUME_STATE = position
            print("Volume Down")
            for _ in range(abs(delta)):
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                time.sleep(0.1)  # Add a small delay between decrements
            # Additional logic for volume down can be added here if needed

def play_pause():
    global switch_last_state
    global switch_last_time

    switch_state = switch.value

    # Check for a change in switch state
    if switch_state != switch_last_state:
        # Record the time when the switch changes state
        switch_last_time = time.monotonic()

    # If the switch state has been stable for a while, register the press
    if time.monotonic() - switch_last_time > DEBOUNCE_DELAY_ENCODER:
        if not switch_state:  # Check if the switch is pressed
            # Toggle play/pause state
            cc.send(ConsumerControlCode.PLAY_PAUSE)
            time.sleep(0.1)

    # Update the last switch state
    switch_last_state = switch_state
    
def handle_key_press(key_number):
    global current_mode
    
    # Define actions for each key number
    # Action for key 0: Type 'A'
    if current_mode == MODE_BLENDER:
        if key_number == 0:
            print("Typing 'tab'")
            kbd.press(Keycode.TAB)
        elif key_number == 1:
            # Action for key 1: Type 'B'
            print("Typing 'B'")
            kbd.press(Keycode.B)
        elif key_number == 2:
            # Action for key 2: Type 'C'
            print("Typing 'G'")
            kbd.press(Keycode.G)
        elif key_number == 3:
            # Action for key 3: Type 'D'
            print("Typing 'R'")
            kbd.press(Keycode.R)
        elif key_number == 4:
            # Action for key 4: Type 'E'
            print("Typing 'S'")
            kbd.press(Keycode.S)
        elif key_number == 5:
            # Action for key 6: Type 'G'
            print("Typing 'O'")
            kbd.press(Keycode.O)
        elif key_number == 6:
            # Action for key 6: Type 'G'
            print("Typing 'E'")
            kbd.press(Keycode.E)
        elif key_number == 7:
            # Action for key 6: Type 'G'
            print("Typing 'I'")
            kbd.press(Keycode.I)
        elif key_number == 8:
            # Action for key 6: Type 'G'
            print("Typing 'X'")
            kbd.press(Keycode.X)
        elif key_number == 9:
            # Action for key 6: Type 'G'
            print("Typing 'Y'")
            kbd.press(Keycode.Y)
        elif key_number == 10:
            # Action for key 6: Type 'G'
            print("Typing 'Z'")
            kbd.press(Keycode.Z)
        elif key_number == 11:
            # Action for key 6: Type 'G'
            print("Typing 'undo'")
            kbd.press(Keycode.CONTROL, Keycode.Z)
        elif key_number == 12:
            # Action for key 6: Type 'G'
            print("Typing 'ZERO'")
            kbd.press(Keycode.KEYPAD_ZERO)
        elif key_number == 13:
            # Action for key 6: Type 'G'
            print("Typing 'NUM .'")
            kbd.press(Keycode.KEYPAD_PERIOD)
        elif key_number == 14:
            # Action for key 6: Type 'G'
            print("1'")
            kbd.press(Keycode.ONE)
        elif key_number == 15:
            # Action for key 6: Type 'G'
            print("Typing '2'")
            kbd.press(Keycode.TWO)
        elif key_number == 16:
            # Action for key 6: Type 'G'
            print("Typing '3'")
            kbd.press(Keycode.THREE)
        elif key_number == 17:
            # Action for key 6: Type 'G'
            print("Typing 'CRTL + Z'")
            kbd.press(Keycode.CONTROL, Keycode.ALT, Keycode.Z)
        elif key_number == 18:
            # Action for key 6: Type 'G'
            print("Typing 'shift'")
            kbd.press(Keycode.SHIFT)
        elif key_number == 19:
            # Action for key 6: Type 'G'
            print("Typing 'SHIFT +ALT'")
            kbd.press(Keycode.SHIFT, Keycode.ALT)
        elif key_number == 20:
            # Action for key 6: Type 'G'
            print("Typing 'A'")
            kbd.press(Keycode.A)
        elif key_number == 21:
            # Action for key 6: Type 'G'
            print("Typing 'SHIFT + A'")
            kbd.press(Keycode.SHIFT, Keycode.A)
        elif key_number == 22:
            # Action for key 6: Type 'G'
            print("Typing 'loop cut'")
            kbd.press(Keycode.CONTROL, Keycode.R)
        elif key_number == 23:
            # Action for key 6: Type 'G'
            print("Typing 'CRTL + SAVE'")
            kbd.press(Keycode.CONTROL, Keycode.S)

    elif current_mode == MODE_KRITA:
        # Handle key presses in CAPSLOCK mode
        if key_number == 0:
            print("Typing 'tab'")
            kbd.press(Keycode.TAB)
        elif key_number == 1:
            # Action for key 1: Type 'B'
            print("Typing 'B'")
            kbd.press(Keycode.B)
        elif key_number == 2:
            # Action for key 2: Type 'C'
            print("Typing 'G'")
            kbd.press(Keycode.CONTROL, Keycode.T)
        elif key_number == 3:
            # Action for key 3: Type 'D'
            print("Typing 'R'")
            kbd.press(Keycode.CONTROL, Keycode.A)
        elif key_number == 4:
            # Action for key 4: Type 'E'
            print("Typing 'S'")
            kbd.press(Keycode.CONTROL, Keycode.J)
        elif key_number == 5:
            # Action for key 6: Type 'G'
            print("Typing 'O'")
            kbd.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.N)
        elif key_number == 6:
            # Action for key 6: Type 'G'
            print("Typing 'E'")
            kbd.press(Keycode.CONTROL)
        elif key_number == 7:
            # Action for key 6: Type 'G'
            print("Typing '1'")
            kbd.press(Keycode.N)
        elif key_number == 8:
            # Action for key 6: Type 'G'
            print("Typing '2'")
            kbd.press(Keycode.M)
        elif key_number == 9:
            # Action for key 6: Type 'G'
            print("Typing '3'")
            kbd.press(Keycode.K)
        elif key_number == 10:
            # Action for key 6: Type 'G'
            print("Typing '4'")
            kbd.press(Keycode.CONTROL, Keycode.D)
        elif key_number == 11:
            # Action for key 6: Type 'G'
            print("Typing 'C'")
            kbd.press(Keycode.CONTROL, Keycode.Z)
        elif key_number == 12:
            # Action for key 6: Type 'G'
            print("Typing 'ESC'")
            kbd.press(Keycode.F)
        elif key_number == 13:
            # Action for key 6: Type 'G'
            print("Typing 'NUM .'")
            kbd.press(Keycode.E)
        elif key_number == 14:
            # Action for key 6: Type 'G'
            print("Q'")
            kbd.press(Keycode.B)
        elif key_number == 15:
            # Action for key 6: Type 'G'
            print("Typing 'W'")
            kbd.press(Keycode.LEFT_BRACKET)
        elif key_number == 16:
            # Action for key 6: Type 'G'
            print("Typing 'E'")
            kbd.press(Keycode.RIGHT_BRACKET)
        elif key_number == 17:
            # Action for key 6: Type 'G'
            print("Typing 'CRTL + Z'")
            kbd.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.Z)
        elif key_number == 18:
            # Action for key 6: Type 'G'
            print("Typing 'SPACE'")
            kbd.press(Keycode.SPACE)
        elif key_number == 19:
            # Action for key 6: Type 'G'
            print("Typing 'A'")
            kbd.press(Keycode.CONTROL, Keycode.SPACE)
        elif key_number == 20:
            # Action for key 6: Type 'G'
            print("Typing 'S'")
            kbd.press(Keycode.SHIFT, Keycode.SPACE)
        elif key_number == 21:
            # Action for key 6: Type 'G'
            print("Typing 'D'")
            kbd.press(Keycode.COMMA)
        elif key_number == 22:
            # Action for key 6: Type 'G'
            print("Typing 'loop cut'")
            kbd.press(Keycode.PERIOD, Keycode.R)
        elif key_number == 23:
            # Action for key 6: Type 'G'
            print("Typing 'CRTL + SAVE'")
            kbd.press(Keycode.CONTROL, Keycode.S)


def switch_mode():
    global current_mode

    # Check if specific keys are pressed for mode switching
    event = matrix.events.get()
    if event and event.pressed:
        key_number = event.key_number
        current_mode = (current_mode + 1) % 3  # Switch between MODE_NORMAL, MODE_CAPSLOCK, and MODE_MEDIA
        print(f"Switched to mode {current_mode}")


def loop():
    global current_mode

    try:
        # Rotation
        volume_control(encoder.position)

        # Keypad input
        keypad_input()

        # Play/Pause with encoder button
        play_pause()
        
        # Mode selection with second encoder
        mode_delta = encoder_mode.position
        if mode_delta != 0:
            global current_mode  # Add this line to declare current_mode as a global variable
            # Change the direction of mode cycle
            current_mode = (current_mode - mode_delta) % 3
            encoder_mode.position = 0  # Reset position after mode change
            print(f"Switched to mode {current_mode}")


        # Display selected mode on LCD
        display.clear()
        if current_mode == MODE_BLENDER:
            display.print("Mode: BLENDER")
        elif current_mode == MODE_KRITA:
            display.print("Mode: KRITA")
        elif current_mode == MODE_MEDIA:
            display.print("Mode: Media")
        display.set_cursor_pos(1, 0)
        display.print("Encoder: {}".format(encoder.position))
        time.sleep(0.1)
        
    except Exception as e:
        print("An error in the loop occurred: {}".format(e))


if __name__ == "__main__":
    while True:
        try:
            loop()
        except Exception as e:
            print("An error in the main loop occurred: {}".format(e))
