import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Кнопка на GP24 (вбудована)
btn = digitalio.DigitalInOut(board.GP24)
btn.switch_to_input(pull=digitalio.Pull.UP)

# LED індикатор
led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

# HID клавіатура
kbd = Keyboard(usb_hid.devices)

# Стан клавіші
was_pressed = False

while True:
    pressed = not btn.value  # кнопка натиснута, якщо LOW

    if pressed and not was_pressed:
        # початок натискання
        kbd.press(Keycode.SPACE)
        led.value = True
        was_pressed = True

    elif not pressed and was_pressed:
        # відпускання кнопки
        kbd.release(Keycode.SPACE)
        led.value = False
        was_pressed = False

    time.sleep(0.005)
