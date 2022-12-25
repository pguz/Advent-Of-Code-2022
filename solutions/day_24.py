# Day 24: Blizzard Basin

import numpy as np
import pandas as pd


def parse_file(fd):
    board_input = pd.read_csv(fd, header=None, dtype=str).squeeze("columns")
    board = pd.DataFrame(list(board_input.map(list)))
    board_wo_borders = board.iloc[1:-1, 1:-1]
    src = (0, 1)
    dst = (board.index[-1], board.columns[-2])
    blizs = [
        board_wo_borders == "^",
        board_wo_borders == "v",
        board_wo_borders == ">",
        board_wo_borders == "<",
    ]
    return (src, dst, *blizs)


def _fastest_path(src, dst, up_bliz, down_bliz, right_bliz, left_bliz):
    bliz_map = up_bliz | down_bliz | right_bliz | left_bliz
    queue = [(src, 1)]
    state = {(src, 1)}
    prev_time = 0
    bliz_cols = list(right_bliz.columns)
    right_bliz_cols_after = bliz_cols[-1:] + bliz_cols[:-1]
    left_bliz_cols_after = bliz_cols[1:] + bliz_cols[:1]
    while queue:
        coord, time_ = queue.pop(0)
        assert prev_time <= time_ and time_ <= prev_time + 1

        if prev_time < time_:
            up_bliz = up_bliz.apply(np.roll, shift=-1)
            down_bliz = down_bliz.apply(np.roll, shift=1)
            right_bliz = right_bliz[right_bliz_cols_after]
            left_bliz = left_bliz[left_bliz_cols_after]
            right_bliz.columns = bliz_cols
            left_bliz.columns = bliz_cols
            bliz_map = up_bliz | down_bliz | right_bliz | left_bliz
            prev_time = time_

        for next_coord in [
            coord,
            (coord[0] - 1, coord[1]),
            (coord[0] + 1, coord[1]),
            (coord[0], coord[1] - 1),
            (coord[0], coord[1] + 1),
        ]:
            if next_coord == dst:
                return time_, up_bliz, down_bliz, right_bliz, left_bliz
            if (next_coord, time_ + 1) in state:
                continue
            if next_coord == src:
                state.add((next_coord, time_ + 1))
                queue.append((next_coord, time_ + 1))
                continue
            if not (
                next_coord[0] in bliz_map.index and next_coord[1] in bliz_map.columns
            ):
                continue
            if bliz_map.loc[next_coord]:
                continue
            state.add((next_coord, time_ + 1))
            queue.append((next_coord, time_ + 1))


def fastest_path(src, dst, *blizs):
    return _fastest_path(src, dst, *blizs)[0]


def fastest_path_with_return(src, dst, *blizs):
    t1, *blizs = _fastest_path(src, dst, *blizs)
    src, dst = dst, src
    t2, *blizs = _fastest_path(src, dst, *blizs)
    src, dst = dst, src
    t3, *_ = _fastest_path(src, dst, *blizs)
    return t1 + t2 + t3


solution_function_01 = fastest_path
solution_function_02 = fastest_path_with_return
