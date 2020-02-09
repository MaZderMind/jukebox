from color_utils import generate_color_steps
from reverse_repeat import ReverseRepeatIterator

ROWS = 15
LEDS_PER_ROW = 11
FPS = 30


def build_iterator(colors, speed, direction, lower_limit):
    num_steps = calculate_steps(speed, lower_limit)
    color_steps = generate_color_steps(colors, num_steps)
    color_sequence_iterator = ReverseRepeatIterator(color_steps, direction)
    return color_sequence_iterator


def calculate_steps(speed, lower_limit):
    """
    speed ranges from (excluding) 0.0 to 1.0
    """
    return max(lower_limit, int(lower_limit * (1 / speed)))
