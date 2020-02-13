import random

from animations.animation_color_wipe import horizontal_wipe, vertical_wipe
from animations.color_utils import from_hex
from animations.direction import Direction


def country():
    colors = [
        from_hex('#ff0000'),
        from_hex('#ffff00'),
    ]
    return random.choice([
        vertical_wipe(colors, speed=0.25, direction=Direction.FORWARD),
        vertical_wipe(colors, speed=0.25, direction=Direction.REVERSE),
        horizontal_wipe(colors, speed=0.25, direction=Direction.FORWARD),
        horizontal_wipe(colors, speed=0.25, direction=Direction.REVERSE),
    ])
