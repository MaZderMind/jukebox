from animations.animation_utils import build_iterator, ROWS, LEDS_PER_ROW
from animations.direction import Direction


def vertical_wipe(colors, speed=0.5, direction=Direction.FORWARD):
    color_sequence_iterator = build_iterator(colors, speed, direction, LEDS_PER_ROW)

    for color_sequence in color_sequence_iterator:
        frame = []

        for row in range(ROWS):
            for color in color_sequence[0:LEDS_PER_ROW]:
                frame += (color,)

        yield frame


def horizontal_wipe(colors, speed=0.1, direction=Direction.FORWARD):
    color_sequence_iterator = build_iterator(colors, speed, direction, ROWS)

    for color_sequence in color_sequence_iterator:
        frame = []

        for row in range(ROWS):
            frame += (color_sequence[row],) * LEDS_PER_ROW

        yield frame
