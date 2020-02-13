from animations.dip_utils import dip_over_black

a = ((1, .5, .5), (.5, 0, .5))
b = ((1, 1, 1), (0, 1, 0))


def test_dip_over_black():
    assert dip_over_black(a, b, 0.00) == ((1.0, 0.50, 0.50), (0.50, 0.0, 0.50))
    assert dip_over_black(a, b, 0.25) == ((0.5, 0.25, 0.25), (0.25, 0.0, 0.25))
    assert dip_over_black(a, b, 0.50) == ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    assert dip_over_black(a, b, 0.75) == ((0.5, 0.5, 0.5), (0.0, 0.5, 0.0))
    assert dip_over_black(a, b, 1.00) == ((1.0, 1.0, 1.0), (0.0, 1.0, 0.0))
