#!/usr/bin/env python3
import asyncio
import random

from animation_color_wipe import vertical_wipe, horizontal_wipe
from animation_stars import stars
from color_utils import from_hex, clamp
from dip_utils import dip_direct
from direction import Direction
from timing import run_animation_sequence

colors = [
    from_hex("FF0000"),
    from_hex("FFA500"),
    from_hex("FFFF00"),
    from_hex("008000"),
    from_hex("0000FF"),
    from_hex("4B0082"),
    from_hex("EE82EE"),
]

light_colors = [
    tuple(clamp(i + 0.5) * 0.75 for i in color)
    for color in colors
]


def random_shift(colors):
    for _ in range(0, random.randint(0, len(colors))):
        colors.insert(0, colors.pop())
    return colors


async def main():
    await run_animation_sequence([
        vertical_wipe(colors, speed=0.25, direction=Direction.FORWARD),
        stars(150, colors=colors, speed=0.75),
        horizontal_wipe(colors, speed=0.25, direction=Direction.FORWARD),
        stars(200, speed=0.01)
    ], seconds_per_animation=5, fade_function=dip_direct)

    while True:
        # await stars(200, speed=0.01)  # slow stars
        # await stars(175, colors=((.5, .5, 1), (1, .5, .5), (1, 1, .5),), speed=0.75)  # flashlights
        # await stars(500, colors=colors, speed=0.2)  # color dots

        # await horizontal_wipe((from_hex("000000"), from_hex("ffffff")), speed=0.95, direction=Direction.REVERSE)

        # rainbows
        # await vertical_wipe(colors, speed=0.25, direction=Direction.FORWARD)
        # await vertical_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.REVERSE)
        # await horizontal_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.FORWARD)
        # await horizontal_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.REVERSE)

        await vertical_wipe(light_colors, speed=0.1, direction=Direction.FORWARD)  # slow and light fade
        # await vertical_wipe(random_shift(colors), speed=0.01, direction=Direction.FORWARD)  # very slow color fade


asyncio.run(main())
