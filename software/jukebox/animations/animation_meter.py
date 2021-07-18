import random

from animations.animation import Animation
from animations.animation_utils import FPS
from animations.color_utils import clamp


class Meter(Animation):
    def __init__(self, bpm=120, color_low=(0, 1, 0), color_mid=(1, 1, 0), color_high=(1, 0, 0)):
        self.bpm = bpm

        bps = int(bpm / 60)
        self.frames_per_beat = int(FPS / bps)

        self.color_low = color_low
        self.color_mid = color_mid
        self.color_high = color_high

    def matrix_generator(self, rows, leds_per_row):
        original_distribution = [random.uniform(0.3, 1) for _ in range(rows)]

        while True:
            distribution = [clamp(
                row + random.uniform(-0.3, 0.3)
            ) for row in original_distribution]

            for _ in range(self.frames_per_beat):
                frame = []
                for row in distribution:
                    on = int(row * leds_per_row)
                    off, high, mid, low = calculate_led_counts(on, leds_per_row)

                    frame += ((0, 0, 0),) * off
                    frame += (self.color_high,) * high
                    frame += (self.color_mid,) * mid
                    frame += (self.color_low,) * low

                distribution = [clamp(
                    row - 0.025 + random.uniform(-0.05, 0.05)
                ) for row in distribution]

                yield frame


def calculate_led_counts(on, leds_per_row):
    low = min(6, on)
    mid = min(3, max(0, on - 6))
    high = max(0, on - 9)
    off = leds_per_row - on
    return off, high, mid, low
