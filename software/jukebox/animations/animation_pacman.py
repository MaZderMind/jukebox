import random

from animations.animation import Animation
from animations.animation_utils import LEDS_PER_ROW, ROWS
from animations.color_utils import linear_interpolate_frame

INITIAL_PLAYFIELD = """
###############
#...#######...#
#.............#
#.#...###...#.#
#.#. ..#....#.#
#.  ..ABC.....#
#......D......#
#.###.###.###.#
#.#.........#.#
#......#......#
###############
"""

COLOR_BORDER = (0, 0, 1)
COLOR_FOOD = (.6, .4, 0)
COLOR_GHOST = {
    "A": (1, 0, 0),
    "B": (0, 1, 1),
    "C": (0, 1, 0),
    "D": (1, 0, 1)
}
COLOR_PACMAN = (1, 1, 0)
COLOR_BACKGROUND = (0, 0, 0)


def playfield_codepoint_to_pixel(codepoint):
    if codepoint == '#':
        return COLOR_BORDER
    elif codepoint == '.':
        return COLOR_FOOD
    elif codepoint.upper() in "ABCD":
        return COLOR_GHOST[codepoint.upper()]
    elif codepoint == 'P':
        return COLOR_PACMAN
    else:
        return COLOR_BACKGROUND


def playfield_to_frame(playfield):
    return [
        playfield_codepoint_to_pixel(codepoint) for codepoint in playfield
    ]


def rotate_frame(frame):
    rotated = [
        frame[col * ROWS + row]
        for row in range(0, ROWS)
        for col in range(0, LEDS_PER_ROW)

    ]
    return rotated


def place_pacman(playfield):
    while True:
        idx = random.randint(0, len(playfield) - 1)
        if playfield[idx] == '.':
            playfield[idx] = 'P'
            return


class GameOverException(Exception):
    pass


def move_character(playfield, character, is_pacman, last_direction):
    # lower denotes no food underneath
    try:
        idx = playfield.index(character.lower())
    except ValueError:
        idx = playfield.index(character.upper())

    has_food_underneath = playfield[idx] == character.upper()
    last_direction = last_direction or 0

    movements = {
        0: - ROWS,  # up
        1: + 1,  # right
        2: + ROWS,  # down
        3: - 1,  # left
    }

    def has_food(direction):
        new_idx = idx + movements[direction % 4]
        return 0 < new_idx < len(playfield) and playfield[new_idx] == "."

    def update_playfield_if_valid(direction):
        new_idx = idx + movements[direction % 4]
        new_has_food_underneath = playfield[new_idx] == "."

        if 0 < new_idx < len(playfield) and playfield[new_idx] in " .P":
            if is_pacman:
                playfield[idx] = " "
                playfield[new_idx] = character
            else:
                if playfield[new_idx] == 'P':
                    playfield[new_idx] = character.upper() if new_has_food_underneath else character.lower()
                    raise GameOverException()

                playfield[idx] = "." if has_food_underneath else " "
                playfield[new_idx] = character.upper() if new_has_food_underneath else character.lower()

            return True

    # try last direction
    if update_playfield_if_valid(last_direction):
        return last_direction

    has_food_right = has_food(last_direction + 1)
    preferrs_left = random.choice([True, False])

    # try right turn for food
    if has_food_right and update_playfield_if_valid(last_direction + 1):
        return last_direction + 1

    # try left turn for preferrence
    if preferrs_left and update_playfield_if_valid(last_direction - 1):
        return last_direction - 1

    # try unconditional right turn
    if update_playfield_if_valid(last_direction + 1):
        return last_direction + 1

    # try unconditional left turn
    if update_playfield_if_valid(last_direction + 1):
        return last_direction + 1

    # try reverse
    if update_playfield_if_valid(last_direction + 2):
        return last_direction + 2


class Pacman(Animation):
    def matrix_generator(self, rows, leds_per_row):
        n_leds = rows * leds_per_row
        last_frame = None
        while True:
            try:
                gameframe = pacman_gameframe_generator()
                while True:
                    last_frame = next(gameframe)
                    yield last_frame
            except GameOverException:
                n_fade = 25
                for frame in range(n_fade):
                    yield linear_interpolate_frame(last_frame, ((0, 0, 0),) * n_leds, frame / n_fade)

    def strip_generator(self, leds):
        n_pacman = 5
        position = 0
        direction = +1
        while True:
            yield \
                (COLOR_BORDER,) + \
                (COLOR_BACKGROUND,) * (position + 1) + \
                (COLOR_PACMAN,) * n_pacman + \
                (COLOR_BACKGROUND,) * (leds - position - n_pacman - 3) + \
                (COLOR_BORDER,)

            position += direction
            if position == leds - n_pacman - 3:
                direction = -1
            elif position == 0:
                direction = +1


def pacman_gameframe_generator():
    playfield = [char for char in INITIAL_PLAYFIELD.replace('\n', '').replace('\r', '')]
    place_pacman(playfield)
    frame_count = 0
    pacman_last_direction = None
    ghost_last_direction = {
        'A': None,
        'B': None,
        'C': None,
        'D': None,
    }

    while True:
        frame_count += 1
        if frame_count == 10:
            frame_count = 0
            pacman_last_direction = move_character(playfield, 'P', True, pacman_last_direction)
            for ghost in 'ABCD':
                ghost_last_direction[ghost] = move_character(playfield, ghost, False, ghost_last_direction[ghost])

        yield rotate_frame(playfield_to_frame(playfield))
