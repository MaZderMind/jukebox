import asyncio
from datetime import datetime, timedelta

from color_utils import generate_color_steps, to_byte, rgb_gamma
from direction import Direction
from reverse_repeat import ReverseRepeatIterator
from send import send

ROWS = 15
LEDS_PER_ROW = 11
FPS = 30


async def vertical_wipe(colors, speed=0.5, stop_after_seconds=False, direction=Direction.FORWARD):
    color_sequence_iterator = await build_iterator(colors, speed, direction, LEDS_PER_ROW)

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


async def horizontal_wipe(colors, speed=1.0, stop_after_seconds=False, direction=Direction.FORWARD):
    color_sequence_iterator = await build_iterator(colors, speed, direction, ROWS)

    start = datetime.now()
    for color_sequence in color_sequence_iterator:
        msg = b''

        for row in range(ROWS):
            msg += bytes(to_byte(rgb_gamma(color_sequence[row])) * LEDS_PER_ROW)

        send(msg)
        await asyncio.sleep(1 / FPS)
        if is_timed_out(start, stop_after_seconds):
            break


async def build_iterator(colors, speed, direction, lower_limit):
    num_steps = calculate_steps(speed, lower_limit)
    color_steps = generate_color_steps(colors, num_steps)
    color_sequence_iterator = ReverseRepeatIterator(color_steps, direction)
    return color_sequence_iterator


def calculate_steps(speed, lower_limit):
    """
    speed ranges from (excluding) 0.0 to 1.0
    """
    return max(lower_limit, int(lower_limit * (1 / speed)))


def is_timed_out(start, stop_after_seconds):
    return stop_after_seconds is not False and datetime.now() - start > timedelta(seconds=stop_after_seconds)
