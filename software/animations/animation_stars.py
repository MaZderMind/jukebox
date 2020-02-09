import random

from animation_utils import ROWS, LEDS_PER_ROW
from color_utils import multiply, clamp
from direction import Direction

N_LEDS = ROWS * LEDS_PER_ROW


class Star(object):
    def __init__(self, color):
        self.color = color
        self.position = int(random.uniform(0, N_LEDS))
        self.fixed = n_percent(10)
        self.current_brightness = random.uniform(-1.0, 1.0)
        self.direction = Direction.FORWARD if n_percent(50) else Direction.REVERSE
        self.individual_speed = random.uniform(0.3, 1.0)

    def increment(self, speed):
        delta = speed * self.individual_speed
        self.current_brightness += delta if self.direction == Direction.FORWARD else -delta

        if self.current_brightness >= 1.0:
            self.direction = Direction.REVERSE
        elif self.current_brightness <= -1.0:
            self.direction = Direction.FORWARD


def stars(amount, colors=((1.0, 1.0, 1.0),), speed=1.0):
    star_objects = [Star(random.choice(colors)) for _ in range(amount)]

    while True:
        frame = [(0, 0, 0)] * N_LEDS

        for star in star_objects:
            if not star.fixed:
                star.increment(speed)

            frame[star.position] = clamp(multiply(star.color, star.current_brightness))

        yield frame


def n_percent(n):
    return random.randint(0, 100) < n
