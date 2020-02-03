from collections import Iterable


def all_channels(func):
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


@all_channels
def to_ff(x):
    """ Returns a sRGB value in the range [0,255]
        for linear input in [0,1]
        Can be called with a single Value or with an (R,G,B)-Tuple
    """
    return min(int(256 * x), 255)


@all_channels
def from_ff(x):
    """ Returns a sRGB value in the range [0,255]
        for linear input in [0,1]
        Can be called with a single Value or with an (R,G,B)-Tuple
    """
    return x / 255.0


@all_channels
def from_srgb(x):
    """ Returns a linear value in the range [0,1]
        for sRGB input in [0,255].
        Can be called with a single Value or with an (R,G,B)-Tuple
    """
    x /= 255.0
    if x <= 0.04045:
        y = x / 12.92
    else:
        y = ((x + 0.055) / 1.055) ** 2.4
    return y


def all_channels_two_colors(func):
    def wrapper(channels1, channels2, *args, **kwargs):
        if isinstance(channels1, tuple) and isinstance(channels2, tuple):
            return tuple(
                func(channel1, channel2, *args, **kwargs)
                for channel1, channel2 in zip(channels1, channels2)
            )
        else:
            return func(channels1, channels2, *args, **kwargs)

    return wrapper


@all_channels_two_colors
def linear_interpolate(color1, color2, frac):
    return color1 * (1 - frac) + color2 * frac


def steps(color1, color2, steps):
    color1_01 = from_ff(color1)
    color2_01 = from_ff(color2)

    return [
        to_ff(
            linear_interpolate(color1_01, color2_01, step / (steps - 1))
        )
        for step in range(steps)
    ]


def rgb_gamma(color):
    gamma = .43

    r_correction = 1.0
    g_correction = 0.8
    b_correction = 0.8

    return (
        int((color[0] / 255) ** (1 / gamma) * r_correction * 255),
        int((color[1] / 255) ** (1 / gamma) * g_correction * 255),
        int((color[2] / 255) ** (1 / gamma) * b_correction * 255)
    )
