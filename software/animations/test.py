#!/usr/bin/env python3
import time

from color_utils import steps, rgb_gamma
from reverse_repeat import ReverseRepeatIterator
from send import send

c1 = (255, 0, 0)
c2 = (0, 0, 255)

rows = 15
leds_per_row = 11
color_steps = steps(c1, c2, 30)
repeating_iterator = ReverseRepeatIterator(color_steps)

for colorset in repeating_iterator:
    msg = b''
    for _ in range(rows):
        for color in colorset[0:leds_per_row]:
            msg += bytes(rgb_gamma(color))

    send(msg)
    time.sleep(1 / 30)
