import random

from animations.animation_utils import ROWS, FPS, LEDS_PER_ROW
from animations.color_utils import clamp


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
                on = int(row * LEDS_PER_ROW)
                off, high, mid, low = calculate_led_counts(on)

                frame += ((0, 0, 0),) * off
                frame += (color_high,) * high
                frame += (color_mid,) * mid
                frame += (color_low,) * low

            distribution = [clamp(
                row - 0.025 + random.uniform(-0.05, 0.05)
            ) for row in distribution]

            yield frame


def calculate_led_counts(on):
    low = min(6, on)
    mid = min(3, max(0, on - 6))
    high = max(0, on - 9)
    off = LEDS_PER_ROW - on
    return off, high, mid, low
