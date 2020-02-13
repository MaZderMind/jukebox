import random

from animations import animation_solid
from animations.animation_color_wipe import horizontal_wipe, vertical_wipe
from animations.animation_meter import meter
from animations.animation_pacman import pacman
from animations.animation_stars import stars
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
        pacman(),
        pacman(),
        meter(),
        meter(),
        stars(500, colors=rainbow, speed=0.2),
        vertical_wipe(rainbow, speed=0.5, direction=Direction.FORWARD),
        vertical_wipe(rainbow, speed=0.5, direction=Direction.REVERSE),
        horizontal_wipe(rainbow, speed=0.5, direction=Direction.FORWARD),
        horizontal_wipe(rainbow, speed=0.5, direction=Direction.REVERSE),
    ])


def slow():
    return random.choice([
        stars(150, colors=rainbow, speed=0.01),
        stars(150, colors=[(1, .4, 0)], speed=0.01),
        stars(150, colors=[(0, 1, 0)], speed=0.01),
        stars(150, colors=[(1, 0, 1)], speed=0.01),
        stars(150, colors=[(0, 1, 1)], speed=0.01),
        vertical_wipe([(1, 0, 0), (0, 0, 1)], speed=0.5, direction=Direction.FORWARD),
        vertical_wipe([(0, 1, 0), (0, 0, 1)], speed=0.5, direction=Direction.REVERSE),
        horizontal_wipe([(0, 1, 0), (1, 1, 0)], speed=0.5, direction=Direction.FORWARD),
        horizontal_wipe(rainbow, speed=0.1, direction=Direction.REVERSE),
    ])


def fast():
    return random.choice([
        pacman(),
        stars(175, colors=((.5, .5, 1), (1, .5, .5), (1, 1, .5),), speed=0.3),
        horizontal_wipe((from_hex("000000"), from_hex("ffffff")), speed=0.95, direction=Direction.REVERSE),
        horizontal_wipe([(1, 0, 0), (0, 0, 1)], speed=0.9, direction=Direction.FORWARD),
        horizontal_wipe([(0, 1, 0), (0, 0, 1)], speed=0.9, direction=Direction.REVERSE),
        vertical_wipe([(0, 1, 0), (1, 1, 0)], speed=0.9, direction=Direction.FORWARD),
        vertical_wipe(rainbow, speed=0.5, direction=Direction.REVERSE),
        vertical_wipe(rainbow, speed=0.5, direction=Direction.FORWARD),
    ])


def country():
    colors = [
        from_hex('FF0000'),  # red
        from_hex('FFFF00'),  # yellow
    ]
    return random.choice([
        stars(50, colors=[(1, .6, 0)], speed=0.01),
        stars(150, colors=[(1, 1, 1)], speed=0.01),
        stars(150, colors=[(1, 1, 1)], speed=0.2),
        stars(150, colors=[(1, .4, 0)], speed=0.2),
        vertical_wipe(colors, speed=0.25, direction=Direction.FORWARD),
        vertical_wipe(colors, speed=0.25, direction=Direction.REVERSE),
        horizontal_wipe(colors, speed=0.25, direction=Direction.FORWARD),
        horizontal_wipe(colors, speed=0.25, direction=Direction.REVERSE),
    ])


def solid(color):
    return animation_solid.solid(from_hex(color))
