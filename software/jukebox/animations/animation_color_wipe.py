from animations.animation import Animation
from animations.animation_utils import build_iterator
from animations.direction import Direction


class VerticalWipe(Animation):
    def __init__(self, colors, speed=0.5, direction=Direction.FORWARD):
        self.direction = direction
        self.speed = speed
        self.colors = colors

    def matrix_generator(self, rows, leds_per_row, speed_factor=1.0):
        color_sequence_iterator = build_iterator(self.colors, self.speed * speed_factor, self.direction, leds_per_row)

        for color_sequence in color_sequence_iterator:
            frame = []

            for row in range(rows):
                for color in color_sequence[0:leds_per_row]:
                    frame += (color,)

            yield frame

    def strip_generator(self, leds):
        yield from self.matrix_generator(1, leds, speed_factor=2)


class HorizontalWipe(Animation):
    def __init__(self, colors, speed=0.5, direction=Direction.FORWARD):
        self.direction = direction
        self.speed = speed
        self.colors = colors

    def matrix_generator(self, rows, leds_per_row, speed_factor=1.0):
        color_sequence_iterator = build_iterator(self.colors, self.speed * speed_factor, self.direction, rows)

        for color_sequence in color_sequence_iterator:
            frame = []

            for row in range(rows):
                frame += (color_sequence[row],) * leds_per_row

            yield frame

    def strip_generator(self, leds):
        yield from self.matrix_generator(1, leds, speed_factor=1/25)
