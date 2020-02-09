import random

from animation_utils import ROWS, FPS, LEDS_PER_ROW
from color_utils import clamp


def meter(bpm=120, color_low=(0, 1, 0), color_mid=(1, 1, 0), color_high=(1, 0, 0)):
    bps = int(bpm / 60)
    frames_per_beat = int(FPS / bps)
    original_distribution = [random.uniform(0.3, 1) for _ in range(ROWS)]

    while True:
        distribution = [clamp(
            row + random.uniform(-0.3, 0.3)
        ) for row in original_distribution]

        for _ in range(frames_per_beat):
            frame = []
            for row in distribution:
                n_leds_on = int(row * LEDS_PER_ROW)
                n_leds_high = max(0, n_leds_on - 8)
                n_leds_mid = max(0, n_leds_on - 6)
                n_leds_low = n_leds_on - n_leds_high - n_leds_mid
                n_leds_off = LEDS_PER_ROW - n_leds_on

                frame += ((0, 0, 0),) * n_leds_off
                frame += (color_high,) * n_leds_high
                frame += (color_mid,) * n_leds_mid
                frame += (color_low,) * n_leds_low

            distribution = [clamp(
                row - 0.025 + random.uniform(-0.05, 0.05)
            ) for row in distribution]

            yield frame
