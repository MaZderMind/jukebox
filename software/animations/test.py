#!/usr/bin/env python3
import time

from color_utils import steps_two_colors, rgb_gamma, to_byte
from reverse_repeat import ReverseRepeatIterator
from send import send

c1 = (1., 0., 1.)
c2 = (0., 0., 0.)

rows = 15
leds_per_row = 11
color_steps = steps_two_colors(c1, c2, 30)
repeating_iterator = ReverseRepeatIterator(color_steps)

for colorset in repeating_iterator:
    msg = b''
    for _ in range(rows):
        for color in colorset[0:leds_per_row]:
            msg += bytes(to_byte(rgb_gamma(color)))

    send(msg)
    time.sleep(1 / 30)
