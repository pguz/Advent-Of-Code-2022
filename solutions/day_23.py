# Day 23: Unstable Diffusion


import functools
import operator
import pandas as pd


def parse_file(fd):
    return (fd,)


def _handle_one_cycle(dir_offset, area_df):
    dirs = {
        0: {"periods": -1, "axis": 0},
        1: {"periods": 1, "axis": 0},
        2: {"periods": -1, "axis": 1},
        3: {"periods": 1, "axis": 1},
    }

    def proces_dir(dir, area_to_process, dir_empty_area):
        to_move_df = area_to_process & dir_empty_area
        moved_df = to_move_df.shift(**dirs[dir])
        not_moved_df = area_to_process & ~to_move_df
        return moved_df, not_moved_df

    ns_check_area = ~(area_df.shift(**dirs[2]) | area_df | area_df.shift(**dirs[3]))
    we_check_area = ~(area_df.shift(**dirs[0]) | area_df | area_df.shift(**dirs[1]))

    empty_areas = {
        0: ns_check_area.shift(**dirs[1]),
        1: ns_check_area.shift(**dirs[0]),
        2: we_check_area.shift(**dirs[3]),
        3: we_check_area.shift(**dirs[2]),
    }

    stable_points_df = functools.reduce(operator.and_, empty_areas.values())
    area_to_process = area_df & ~stable_points_df

    pos_moved_dfs = {}
    for j in range(4):
        dir = (dir_offset + j) % 4
        pos_moved_df, area_to_process = proces_dir(
            dir, area_to_process, empty_areas[dir]
        )
        pos_moved_dfs[dir] = pos_moved_df

    n_moved_df = pos_moved_dfs[0] & ~(
        pos_moved_dfs[1] | pos_moved_dfs[2] | pos_moved_dfs[3]
    )
    s_moved_df = pos_moved_dfs[1] & ~(
        pos_moved_dfs[0] | pos_moved_dfs[2] | pos_moved_dfs[3]
    )
    w_moved_df = pos_moved_dfs[2] & ~(
        pos_moved_dfs[0] | pos_moved_dfs[1] | pos_moved_dfs[3]
    )
    e_moved_df = pos_moved_dfs[3] & ~(
        pos_moved_dfs[0] | pos_moved_dfs[1] | pos_moved_dfs[2]
    )

    to_move_df = (
        n_moved_df.shift(**dirs[1])
        | s_moved_df.shift(**dirs[0])
        | w_moved_df.shift(**dirs[3])
        | e_moved_df.shift(**dirs[2])
    )

    area_df = (
        (area_df & ~to_move_df) | n_moved_df | s_moved_df | w_moved_df | e_moved_df
    )
    assert area_df.iloc[0, :].sum() == 0
    assert area_df.iloc[-1, :].sum() == 0
    assert area_df.iloc[:, 0].sum() == 0
    assert area_df.iloc[:, -1].sum() == 0

    return area_df


def empty_ground_tiles(area_fd):
    area_data = [
        "......" + line[:-1] + "......" for line in area_fd.readlines()
    ]
    area_data = (
        ["." * len(area_data[0])] * 10
        + area_data
        + ["." * len(area_data[0])] * 10
    )
    area_df = pd.DataFrame(map(list, area_data)).replace({"#": True, ".": False})

    for i in range(10):
        area_df = _handle_one_cycle(dir_offset=i, area_df=area_df)

    while area_df.iloc[0, :].sum() == 0:
        area_df = area_df.iloc[1:, :]
    while area_df.iloc[-1, :].sum() == 0:
        area_df = area_df.iloc[:-1, :]
    while area_df.iloc[:, 0].sum() == 0:
        area_df = area_df.iloc[:, 1:]
    while area_df.iloc[:, -1].sum() == 0:
        area_df = area_df.iloc[:, :-1]

    return (~area_df).sum().sum()


def no_elves_move_round(area_fd):
    area_data = [
        "......" * 10 + line[:-1] + "......" * 10 for line in area_fd.readlines()
    ]
    area_data = (
        ["." * len(area_data[0])] * 100
        + area_data
        + ["." * len(area_data[0])] * 100
    )
    area_df = pd.DataFrame(map(list, area_data)).replace({"#": True, ".": False})

    i = 0
    while True:
        prev_area_df = area_df

        area_df = _handle_one_cycle(dir_offset=i, area_df=area_df)

        if area_df.equals(prev_area_df):
            return i + 1

        i = i + 1


solution_function_01 = empty_ground_tiles
solution_function_02 = no_elves_move_round
