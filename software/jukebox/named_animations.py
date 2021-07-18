import random

from animations.animation_color_wipe import VerticalWipe, HorizontalWipe
from animations.animation_meter import Meter
from animations.animation_pacman import Pacman
from animations.animation_solid import Solid
from animations.animation_stars import Stars
from animations.color_utils import from_hex
from animations.direction import Direction

rainbow = [
    from_hex("FF0000"),
    from_hex("FFA500"),
    from_hex("FFFF00"),
    from_hex("008000"),
    from_hex("0000FF"),
    from_hex("4B0082"),
    from_hex("EE82EE"),
]


def techno():
    return random.choice([
        Pacman(),
        Pacman(),
        Meter(),
        Meter(),
        Stars(500, colors=rainbow, speed=0.2),
        VerticalWipe(rainbow, speed=0.5, direction=Direction.FORWARD),
        VerticalWipe(rainbow, speed=0.5, direction=Direction.REVERSE),
        HorizontalWipe(rainbow, speed=0.5, direction=Direction.FORWARD),
        HorizontalWipe(rainbow, speed=0.5, direction=Direction.REVERSE),
    ])


def slow():
    return random.choice([
        Stars(150, colors=rainbow, speed=0.01),
        Stars(150, colors=[(1, .4, 0)], speed=0.01),
        Stars(150, colors=[(0, 1, 0)], speed=0.01),
        Stars(150, colors=[(1, 0, 1)], speed=0.01),
        Stars(150, colors=[(0, 1, 1)], speed=0.01),
        VerticalWipe([(1, 0, 0), (0, 0, 1)], speed=0.5, direction=Direction.FORWARD),
        VerticalWipe([(0, 1, 0), (0, 0, 1)], speed=0.5, direction=Direction.REVERSE),
        HorizontalWipe([(0, 1, 0), (1, 1, 0)], speed=0.5, direction=Direction.FORWARD),
        HorizontalWipe(rainbow, speed=0.1, direction=Direction.REVERSE),
    ])


def fast():
    return random.choice([
        Pacman(),
        Stars(175, colors=((.5, .5, 1), (1, .5, .5), (1, 1, .5),), speed=0.3),
        HorizontalWipe((from_hex("000000"), from_hex("ffffff")), speed=0.95, direction=Direction.REVERSE),
        HorizontalWipe([(1, 0, 0), (0, 0, 1)], speed=0.9, direction=Direction.FORWARD),
        HorizontalWipe([(0, 1, 0), (0, 0, 1)], speed=0.9, direction=Direction.REVERSE),
        VerticalWipe([(0, 1, 0), (1, 1, 0)], speed=0.9, direction=Direction.FORWARD),
        VerticalWipe(rainbow, speed=0.5, direction=Direction.REVERSE),
        VerticalWipe(rainbow, speed=0.5, direction=Direction.FORWARD),
    ])


def country():
    colors = [
        from_hex('FF0000'),  # red
        from_hex('FFFF00'),  # yellow
    ]
    return random.choice([
        Stars(50, colors=[(1, .6, 0)], speed=0.01),
        Stars(150, colors=[(1, 1, 1)], speed=0.01),
        Stars(150, colors=[(1, 1, 1)], speed=0.2),
        Stars(150, colors=[(1, .4, 0)], speed=0.2),
        VerticalWipe(colors, speed=0.25, direction=Direction.FORWARD),
        VerticalWipe(colors, speed=0.25, direction=Direction.REVERSE),
        HorizontalWipe(colors, speed=0.25, direction=Direction.FORWARD),
        HorizontalWipe(colors, speed=0.25, direction=Direction.REVERSE),
    ])


def solid(color):
    return Solid(from_hex(color))
