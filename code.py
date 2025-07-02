import board
import digitalio
import time
import usb_hid
import json
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Завантаження конфігурації
with open("/config.json", "r") as f:
    config = json.load(f)

# Ініціалізація клавіатури
kbd = Keyboard(usb_hid.devices)

# Підтримувані клавіші
keymap = {
    "SPACE": Keycode.SPACE,
    "ENTER": Keycode.ENTER,
    "A": Keycode.A,
    "B": Keycode.B,
    "C": Keycode.C,
    # додай інші за потреби
}

# Підготовка кнопок
buttons = []
for btn_cfg in config["buttons"]:
    pin = getattr(board, f"GP{btn_cfg['pin']}")
    btn = digitalio.DigitalInOut(pin)
    btn.switch_to_input(pull=digitalio.Pull.UP)
    buttons.append({
        "io": btn,
        "key": keymap[btn_cfg["key"]],
        "was_pressed": False
    })

# LED індикатор
led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()

# Головний цикл
while True:
    for btn in buttons:
        pressed = not btn["io"].value

        if pressed and not btn["was_pressed"]:
            kbd.press(btn["key"])
            led.value = True
            btn["was_pressed"] = True

        elif not pressed and btn["was_pressed"]:
            kbd.release(btn["key"])
            led.value = False
            btn["was_pressed"] = False

    time.sleep(0.005)
