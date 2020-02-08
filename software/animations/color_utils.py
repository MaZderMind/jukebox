import random
from collections.abc import Iterable


def for_each_channel(func):
    def wrapper(channels, *args, **kwargs):
        if isinstance(channels, Iterable):
            # print("is tuple", channels)
            return tuple(
                func(channel, *args, **kwargs)
                for channel in channels
            )
        else:
            # print("is no tuple", channels)
            return func(channels, *args, **kwargs)

    return wrapper


def clamp(v, v_min=0.0, v_max=1.0):
    return max(min(float(v), v_max), v_min)


@for_each_channel
def multiply(v, n):
    """ Returns a value in the range [0,255]
        for linear input in [0,1]
        Can be called with a single Value or with an (R,G,B)-Tuple
    """
    return n * v


@for_each_channel
def to_byte(v):
    """ Returns a value in the range [0,255]
        for linear input in [0,1]
        Can be called with a single Value or with an (R,G,B)-Tuple
    """
    return int(clamp(v) * 255)


@for_each_channel
def from_byte(v):
    """ Returns a value in the range [0,1]
        for linear input in [0,255]
        Can be called with a single Value or with an (R,G,B)-Tuple
    """
    return clamp(v / 255)


def from_hex(hex):
    """ Returns a (R,G,B)-tuple in the range [0,1]
        for a string input in RRGGBB form
    """
    return tuple(
        int(hex[i:i + 2], 16) / 255
        for i in (0, 2, 4)
    )


def for_each_channel_two_args(func):
    def wrapper(channels1, channels2, *args, **kwargs):
        if isinstance(channels1, tuple) and isinstance(channels2, tuple):
            return tuple(
                func(channel1, channel2, *args, **kwargs)
                for channel1, channel2 in zip(channels1, channels2)
            )
        else:
            return func(channels1, channels2, *args, **kwargs)

    return wrapper


@for_each_channel_two_args
def linear_interpolate(color1, color2, frac):
    return color1 * (1 - frac) + color2 * frac


def steps_two_colors(color1, color2, steps):
    return [
        linear_interpolate(color1, color2, step / (steps - 1))
        for step in range(steps)
    ]


def generate_color_steps(colors, steps):
    steps_per_color = equal_distribute(steps, len(colors) - 1)
    pairs = zip(colors[:-1], colors[1:])
    return [
        linear_interpolate(pair[0], pair[1], step / steps_per_color[index])
        for index, pair in enumerate(pairs)
        for step in range(steps_per_color[index])
    ]


def equal_distribute(n, n_bins):
    quotient = n // n_bins
    remainder = n % n_bins

    bins = [quotient for _ in range(n_bins)]
    for i in range(remainder):
        bins[i] += 1

    random.shuffle(bins)
    return bins


def rgb_gamma(color):
    gamma = .43

    r_correction = 1.0
    g_correction = 0.8
    b_correction = 0.8

    if round(color[0], 3) == round(color[1], 3) == round(color[2], 3):
        r_correction = g_correction = b_correction = 0.85

    return (
        color[0] ** (1 / gamma) * r_correction,
        color[1] ** (1 / gamma) * g_correction,
        color[2] ** (1 / gamma) * b_correction,
    )
