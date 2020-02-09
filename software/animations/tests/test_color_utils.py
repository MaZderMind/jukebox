from color_utils import to_byte, clamp, dip_over_black


def test_to_byte():
    assert to_byte(-1.) == 0
    assert to_byte(0.) == 0
    assert to_byte(0.25) == 63
    assert to_byte(0.5) == 127
    assert to_byte(0.75) == 191
    assert to_byte(1.0) == 255
    assert to_byte(1.5) == 255


def test_clamp():
    assert clamp(-10000) == 0.
    assert clamp(-1) == 0.
    assert clamp(-0.1) == 0.
    assert clamp(0.) == 0.
    assert clamp(0.25) == .25
    assert clamp(0.5) == .5
    assert clamp(0.75) == .75
    assert clamp(1.) == 1.
    assert clamp(1.5) == 1.
    assert clamp(100000.) == 1.


a = ((1, .5, .5), (.5, 0, .5))
b = ((1, 1, 1), (0, 1, 0))


def test_dip_over_black():
    assert dip_over_black(a, b, 0.00) == ((1.0, 0.50, 0.50), (0.50, 0.0, 0.50))
    assert dip_over_black(a, b, 0.25) == ((0.5, 0.25, 0.25), (0.25, 0.0, 0.25))
    assert dip_over_black(a, b, 0.50) == ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    assert dip_over_black(a, b, 0.75) == ((0.5, 0.5, 0.5), (0.0, 0.5, 0.0))
    assert dip_over_black(a, b, 1.00) == ((1.0, 1.0, 1.0), (0.0, 1.0, 0.0))
