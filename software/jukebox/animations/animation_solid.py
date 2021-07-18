from animations.animation import Animation


class Solid(Animation):
    def __init__(self, color):
        self.color = color

    def matrix_generator(self, rows, leds_per_row):
        n_leds = rows * leds_per_row
        while True:
            yield (self.color,) * n_leds
