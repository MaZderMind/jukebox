import random

from animation_utils import N_LEDS
from color_utils import multiply, clamp
from direction import Direction


class Star(object):
    def __init__(self, color):
        self.color = color
        self.position = int(random.uniform(0, N_LEDS))
        self.fixed = n_percent(10)
        self.current_brightness = random.uniform(0, 1)
        self.direction = Direction.FORWARD if n_percent(50) else Direction.REVERSE
        self.individual_speed = random.uniform(0.3, 1.0)

    def increment(self, speed):
        if self.fixed:
            return

        delta = speed * self.individual_speed
        self.current_brightness += delta if self.direction == Direction.FORWARD else -delta

        if self.current_brightness >= 1.0:
            self.direction = Direction.REVERSE
        elif self.current_brightness <= 0.0:
            self.position = int(random.uniform(0, N_LEDS))
            self.direction = Direction.FORWARD


def stars(amount, colors=((1.0, 1.0, 1.0),), speed=1.0):
    star_objects = [Star(random.choice(colors)) for _ in range(amount)]

    while True:
        frame = [(0, 0, 0)] * N_LEDS

        for star in star_objects:
            star.increment(speed)
            frame[star.position] = clamp(multiply(star.color, star.current_brightness))

        yield frame


def n_percent(n):
    return random.randint(0, 100) < n
