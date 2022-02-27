import sys
import board
import neopixel
import mido
import time
from enum import Enum


class ColorEffects:
    def __init__(self, count):
        self.count = count

class LedStrip:
    def __init__(self, brightness):
        self.pixels = neopixel.NeoPixel(board.D18, 172, brightness=brightness, auto_write=False, pixel_order=neopixel.GRB)
        self.keys_pressed = 0

    def on(self, key, color):
        self.keys_pressed += 1
        if (self.keys_pressed > 172/2):
            self.pixels.fill(0, 0, 0)

        self.pixels[key] = color

    def off(self, key):
        self.pixels[key] = (0, 0, 0)
        self.keys_pressed -= 1

    def show(self):
        self.pixels.show()

class Keys:
    def __init__(self, color, brightness):
        self.ledstrip = LedStrip(brightness)
        self.color = color
        self.pressed_keys = [Key] * 88

    def key_down(self, key):
        key = key * 2
        self.ledstrip.on(key, self.get_color(key))
        self.ledstrip.on(key + 1, self.get_color(key))
        if (key != 0):
            self.ledstrip.on(key - 1, self.get_color(key))
        self.ledstrip.show()

    def key_up(self, key):
        key = key * 2
        self.ledstrip.off(key)
        self.ledstrip.off(key + 1)
        if (key != 0):
            self.ledstrip.off(key - 1)
        self.ledstrip.show()

    def get_color(self, key):
        return self.color


class Key:
    def __init__(self, key, velocity, time_pressed):
        self.key = key
        self.velocity = velocity
        self.time_pressed = time_pressed


key_counter = 0

msg_buffer = []

args = sys.argv

inport = mido.open_input(mido.get_input_names()[1])

last_frame = time.time()

brightness = 0.5

for i in range(args.__len__()):
    args[i] = args[i].replace(",", "")
    print(args[i])

if (args.__len__() >= 3):
    color = (int(args[1]), int(args[2]), int(args[3]))
    if (args.__len__() >= 4):
        brightness = float(args[4])
        print("brightness", brightness)

else:
    print("no arguments")
    color = (219, 18, 185)

keys = Keys(color, brightness)

last_time = time.time_ns()


while True:
    for event in inport.iter_pending():
        print(event.bytes())
        if (event.bytes()[0] == 144):
            key_counter += 1

            key = event.note - 21
            keys.key_down(key)

        elif (event.bytes()[0] == 128):
            key = event.note - 21
            keys.key_up(key)
