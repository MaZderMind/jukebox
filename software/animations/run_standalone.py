#!/usr/bin/env python3
import asyncio

from animation_pacman import pacman
from color_utils import from_hex, clamp
from timing import run_forever

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


async def main():
    await run_forever(pacman())
    # await run_forever(stars(150, colors=((1., 1., .0),), speed=0.01))  # slow yellow stars
    # await run_forever(stars(150, colors=((1., 1., .0),), speed=0.01))  # slow stars
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
