from animations.color_utils import to_byte, clamp


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
