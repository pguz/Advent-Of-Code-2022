# Day 17: Pyroclastic Flow

import pandas as pd


ROCKS = {
    0: (pd.DataFrame([[False, False, True, True, True, True, False]]), 3),
    1: (
        pd.DataFrame(
            [
                [False, False, False, True, False, False, False],
                [False, False, True, True, True, False, False],
                [False, False, False, True, False, False, False],
            ],
            index=range(-2, 1),
        ),
        4,
    ),
    2: (
        pd.DataFrame(
            [
                [False, False, False, False, True, False, False],
                [False, False, False, False, True, False, False],
                [False, False, True, True, True, False, False],
            ],
            index=range(-2, 1),
        ),
        4,
    ),
    3: (
        pd.DataFrame(
            [
                [False, False, True, False, False, False, False],
                [False, False, True, False, False, False, False],
                [False, False, True, False, False, False, False],
                [False, False, True, False, False, False, False],
            ],
            index=range(-3, 1),
        ),
        6,
    ),
    4: (
        pd.DataFrame(
            [
                [False, False, True, True, False, False, False],
                [False, False, True, True, False, False, False],
            ],
            index=range(-1, 1),
        ),
        5,
    ),
}

EMPTY_BOARD_HEIGHT = 4
BOARD_PROCESSING_HEIGHT = 50


def parse_file(fd):
    dirs = fd.read()
    return (dirs,)


def height_after_2022(dirs):
    board = pd.DataFrame([[False] * 7] * EMPTY_BOARD_HEIGHT + [[True] * 7])
    rock_id = 0
    rock, rock_max_x = ROCKS[0]
    cur_x = 2
    rocks_height = 0
    while True:
        for dir in dirs:
            assert dir in ["<", ">"]

            board_slice = board[min(rock.index[0], 0) : rock.index[-1] + 1]
            if dir == ">" and cur_x < rock_max_x:
                if (rock.shift(1, axis="columns") & board_slice).sum().sum() == 0:
                    rock = rock.shift(1, axis="columns", fill_value=False)
                    cur_x += 1
            elif dir == "<" and cur_x > 0:
                if (rock.shift(-1, axis="columns") & board_slice).sum().sum() == 0:
                    rock = rock.shift(-1, axis="columns", fill_value=False)
                    cur_x -= 1

            rock.index += 1

            board_slice = board[rock.index[0] : rock.index[-1] + 1]
            if (rock & board_slice).sum().sum() == 0:
                continue

            rock.index -= 1
            board = board | rock

            # normalize board - fill safe empty space
            fill_board = EMPTY_BOARD_HEIGHT - rock.index[0]
            if fill_board > 0:
                board.index += fill_board
                board = pd.concat([pd.DataFrame([[False] * 7] * fill_board), board])

            # normalize board - reduce processing board
            if len(board) > BOARD_PROCESSING_HEIGHT:
                rocks_height += len(board) - BOARD_PROCESSING_HEIGHT
                board = board[:BOARD_PROCESSING_HEIGHT]

            if rock_id == 2021:
                return len(board) + rocks_height - 1 - EMPTY_BOARD_HEIGHT

            rock_id = rock_id + 1
            rock, rock_max_x = ROCKS[rock_id % 5]
            cur_x = 2


def height_after_1000000000000(dirs):
    board = pd.DataFrame([[False] * 7] * EMPTY_BOARD_HEIGHT + [[True] * 7])
    rock_id = 0
    rock, rock_max_x = ROCKS[0]
    cur_x = 2
    rocks_height = 0
    state = set()
    max_subsequent_being_in_state = 0
    while True:
        for i, dir in enumerate(dirs):
            assert dir in ["<", ">"]

            board_slice = board[min(rock.index[0], 0) : rock.index[-1] + 1]
            if dir == ">" and cur_x < rock_max_x:
                if (rock.shift(1, axis="columns") & board_slice).sum().sum() == 0:
                    rock = rock.shift(1, axis="columns", fill_value=False)
                    cur_x += 1
            elif dir == "<" and cur_x > 0:
                if (rock.shift(-1, axis="columns") & board_slice).sum().sum() == 0:
                    rock = rock.shift(-1, axis="columns", fill_value=False)
                    cur_x -= 1

            rock.index += 1

            board_slice = board[rock.index[0] : rock.index[-1] + 1]
            if (rock & board_slice).sum().sum() == 0:
                continue

            rock.index -= 1
            board = board | rock

            # normalize board - fill safe empty space
            fill_board = EMPTY_BOARD_HEIGHT - rock.index[0]
            if fill_board > 0:
                board.index += fill_board
                board = pd.concat([pd.DataFrame([[False] * 7] * fill_board), board])

            # normalize board - reduce processing board
            if len(board) > BOARD_PROCESSING_HEIGHT:
                rocks_height += len(board) - BOARD_PROCESSING_HEIGHT
                board = board[:BOARD_PROCESSING_HEIGHT]

            if (i, rock_id % 5) not in state:
                state.add((i, rock_id % 5))
                max_subsequent_being_in_state = 0
            else:
                max_subsequent_being_in_state += 1

            if max_subsequent_being_in_state == 10:
                # later some manual processing
                return (i, rock_id % 5)

            rock_id = rock_id + 1
            rock, rock_max_x = ROCKS[rock_id % 5]
            cur_x = 2


solution_function_01 = height_after_2022
solution_function_02 = height_after_1000000000000
