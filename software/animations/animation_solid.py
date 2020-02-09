from animation_stars import N_LEDS


def solid(color):
    while True:
        yield (color,) * N_LEDS
