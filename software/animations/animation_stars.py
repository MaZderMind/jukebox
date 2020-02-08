import asyncio
import random
from datetime import datetime

from animation_utils import ROWS, LEDS_PER_ROW, FPS, is_timed_out
from color_utils import to_byte, multiply
from direction import Direction
from send import send

N_LEDS = ROWS * LEDS_PER_ROW


class Star(object):
    def __init__(self, color):
        self.color = color
        self.position = int(random.uniform(0, N_LEDS))
        self.fixed = n_percent(10)
        self.current_brightness = random.uniform(-1.0, 1.0)
        self.direction = Direction.FORWARD if n_percent(50) else Direction.REVERSE
        self.individual_speed = random.uniform(0.3, 1.0)

    def increment(self, speed):
        delta = speed * self.individual_speed
        self.current_brightness += delta if self.direction == Direction.FORWARD else -delta

        if self.current_brightness >= 1.0:
            self.direction = Direction.REVERSE
        elif self.current_brightness <= -1.0:
            self.direction = Direction.FORWARD


async def stars(amount, colors=((1.0, 1.0, 1.0),), speed=1.0, stop_after_seconds=False):
    star_objects = [Star(random.choice(colors)) for _ in range(amount)]

    start = datetime.now()
    while True:
        msg = bytearray((0, 0, 0) * N_LEDS)

        for star in star_objects:
            if not star.fixed:
                star.increment(speed)

            index = star.position * 3
            msg[index:index + 3] = to_byte(multiply(star.color, star.current_brightness))

        send(msg)
        await asyncio.sleep(1 / FPS)
        if is_timed_out(start, stop_after_seconds):
            break


def n_percent(n):
    return random.randint(0, 100) < n
