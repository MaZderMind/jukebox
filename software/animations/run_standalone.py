#!/usr/bin/env python3
import asyncio
import random
from asyncio import FIRST_COMPLETED

from animation_color_wipe import vertical_wipe, horizontal_wipe
from animation_stars import stars
from color_utils import from_hex, clamp
from direction import Direction
from timing import Sequencer

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


show_stars = False


def animation_generator():
    global show_stars

    star_generarors = [
        stars(150, colors=colors, speed=0.75),
        stars(200, speed=0.01)
    ]
    non_star_generarors = [
        vertical_wipe(colors, speed=0.25, direction=Direction.FORWARD),
        horizontal_wipe(colors, speed=0.25, direction=Direction.FORWARD)
    ]

    if show_stars:
        return random.choice(star_generarors)
    else:
        return random.choice(non_star_generarors)


sequencer = Sequencer(animation_generator)


async def request_stars():
    global show_stars

    while True:
        await asyncio.sleep(7)
        print("request stars")
        show_stars = True
        sequencer.interrupt()

        await asyncio.sleep(10)
        print("no more stars")
        show_stars = False
        sequencer.interrupt()


async def main():
    await asyncio.wait([
        sequencer.run(),
        request_stars()
    ], return_when=FIRST_COMPLETED)

    # while True:
    # await stars(200, speed=0.01)  # slow stars
    # await stars(175, colors=((.5, .5, 1), (1, .5, .5), (1, 1, .5),), speed=0.75)  # flashlights
    # await stars(500, colors=colors, speed=0.2)  # color dots

    # await horizontal_wipe((from_hex("000000"), from_hex("ffffff")), speed=0.95, direction=Direction.REVERSE)

    # rainbows
    # await vertical_wipe(colors, speed=0.25, direction=Direction.FORWARD)
    # await vertical_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.REVERSE)
    # await horizontal_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.FORWARD)
    # await horizontal_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.REVERSE)

    # await vertical_wipe(light_colors, speed=0.1, direction=Direction.FORWARD)  # slow and light fade
    # await vertical_wipe(random_shift(colors), speed=0.01, direction=Direction.FORWARD)  # very slow color fade


asyncio.run(main())
