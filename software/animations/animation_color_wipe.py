import asyncio
from datetime import datetime

from animation_utils import build_iterator, ROWS, LEDS_PER_ROW, FPS, is_timed_out
from color_utils import to_byte, rgb_gamma
from direction import Direction
from send import send


async def vertical_wipe(colors, speed=0.5, stop_after_seconds=False, direction=Direction.FORWARD):
    color_sequence_iterator = build_iterator(colors, speed, direction, LEDS_PER_ROW)

    start = datetime.now()
    for color_sequence in color_sequence_iterator:
        msg = b''

        for row in range(ROWS):
            for color in color_sequence[0:LEDS_PER_ROW]:
                msg += bytes(to_byte(rgb_gamma(color)))

        send(msg)
        await asyncio.sleep(1 / FPS)
        if is_timed_out(start, stop_after_seconds):
            break


async def horizontal_wipe(colors, speed=0.1, stop_after_seconds=False, direction=Direction.FORWARD):
    color_sequence_iterator = build_iterator(colors, speed, direction, ROWS)

    start = datetime.now()
    for color_sequence in color_sequence_iterator:
        msg = b''

        for row in range(ROWS):
            msg += bytes(to_byte(rgb_gamma(color_sequence[row])) * LEDS_PER_ROW)

        send(msg)
        await asyncio.sleep(1 / FPS)
        if is_timed_out(start, stop_after_seconds):
            break
