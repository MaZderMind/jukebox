#!/usr/bin/env python3
import asyncio

from animation_color_wipe import vertical_wipe, horizontal_wipe
from animation_stars import stars
from color_utils import from_hex
from direction import Direction


async def main():
    colors = [
        from_hex("E70000"),
        from_hex("FF8C00"),
        from_hex("FFEF00"),
        from_hex("00811F"),
        from_hex("0044FF"),
        from_hex("760089"),
    ]

    while True:
        await stars(200, colors, speed=0.8, stop_after_seconds=5)
        await stars(200, speed=0.8, stop_after_seconds=5)
        await stars(200, colors=(from_hex("FF0000"), from_hex("0000FF")), speed=0.8, stop_after_seconds=5)
        await vertical_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.FORWARD)
        await vertical_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.REVERSE)
        await horizontal_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.FORWARD)
        await horizontal_wipe(colors, stop_after_seconds=5, speed=0.25, direction=Direction.REVERSE)


asyncio.run(main())
