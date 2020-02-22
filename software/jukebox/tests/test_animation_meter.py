from animations.animation_meter import calculate_led_counts


def test_calculate_led_counts():
    # off, high, mid, low
    # total = 11
    assert calculate_led_counts(0) == (11, 0, 0, 0)
    assert calculate_led_counts(1) == (10, 0, 0, 1)
    assert calculate_led_counts(2) == (9, 0, 0, 2)
    assert calculate_led_counts(3) == (8, 0, 0, 3)
    assert calculate_led_counts(4) == (7, 0, 0, 4)
    assert calculate_led_counts(5) == (6, 0, 0, 5)
    assert calculate_led_counts(6) == (5, 0, 0, 6)
    assert calculate_led_counts(7) == (4, 0, 1, 6)
    assert calculate_led_counts(8) == (3, 0, 2, 6)
    assert calculate_led_counts(9) == (2, 0, 3, 6)
    assert calculate_led_counts(10) == (1, 1, 3, 6)
    assert calculate_led_counts(11) == (0, 2, 3, 6)
