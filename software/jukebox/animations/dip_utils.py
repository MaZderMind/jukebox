from animations.color_utils import for_each_channel_two_args, linear_interpolate


@for_each_channel_two_args
def dip_over(a, b, color, frac):
    """
    frac is between [0:1]
    during frac [0:0.5] a will be faded to color, during [0.5:1] will faded from color to b
    """
    if frac < 0.5:
        frac *= 2
        return linear_interpolate(a, color, frac)
    else:
        frac = (frac - 0.5) * 2
        return linear_interpolate(color, b, frac)


@for_each_channel_two_args
def dip_direct(a, b, frac):
    return linear_interpolate(a, b, frac)


def dip_over_black(a, b, frac):
    return dip_over(a, b, (0, 0, 0), frac)


def dip_over_white(a, b, frac):
    return dip_over(a, b, (1, 1, 1), frac)
