import random

from animations.animation import Animation
from animations.color_utils import multiply, clamp
from animations.direction import Direction


class Stars(Animation):
    def __init__(self, amount, colors=((1.0, 1.0, 1.0),), speed=1.0):
        self.amount = amount
        self.colors = colors
        self.speed = speed

    def matrix_generator(self, rows, leds_per_row, speed_factor=1.0, amount_factor=1.0):
        n_leds = rows * leds_per_row
        amount = int(self.amount * amount_factor)
        star_objects = [Star(random.choice(self.colors), n_leds) for _ in range(amount)]

        while True:
            frame = [(0, 0, 0)] * n_leds

            for star in star_objects:
                star.increment(self.speed * speed_factor)
                frame[star.position] = clamp(multiply(star.color, star.current_brightness))

            yield frame

    def strip_generator(self, leds):
        yield from self.matrix_generator(1, leds, amount_factor=1/165 * leds)


class Star(object):
    def __init__(self, color, n_leds):
        self.color = color
        self.n_leds = n_leds
        self.position = int(random.uniform(0, n_leds))
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
            self.position = int(random.uniform(0, self.n_leds))
            self.direction = Direction.FORWARD


def n_percent(n):
    return random.randint(0, 100) < n
