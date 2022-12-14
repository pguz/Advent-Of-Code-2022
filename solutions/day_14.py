# Day 14: Regolith Reservoir

import pandas as pd

SAND = "o"
ROCK = "#"
EMPTY = "."
START_POINT = 500


def _process_line(line):
    xs, ys = [], []
    for rock_path in line.split(" -> "):
        x, y = map(int, rock_path.split(","))
        xs.append(x)
        ys.append(y)
    return [min(xs), max(xs), min(ys), max(ys), list(zip(xs, ys))]


def parse_file(fd):
    input_df = pd.Series(fd).map(_process_line).apply(pd.Series)
    return (
        (min(input_df[0]), max(input_df[1])),
        (min(input_df[2]), max(input_df[3])),
        input_df[4],
    )


def _build_area(xs_limits, ys_limits, rock_paths):
    area_df = pd.DataFrame(
        ".",
        index=range(min(0, ys_limits[0]), ys_limits[1] + 1),
        columns=range(xs_limits[0], xs_limits[1] + 1),
    )
    for rock_path in rock_paths:
        for rp_begin, rp_end in zip(rock_path[:-1], rock_path[1:]):
            if rp_begin[0] == rp_end[0]:
                area_df.loc[
                    min(rp_begin[1], rp_end[1]) : max(rp_begin[1], rp_end[1]),
                    rp_begin[0],
                ] = ROCK
            if rp_begin[1] == rp_end[1]:
                area_df.loc[
                    rp_begin[1],
                    min(rp_begin[0], rp_end[0]) : max(rp_begin[0], rp_end[0]),
                ] = ROCK
    return area_df


def _handle_sand(area_df):
    cy, cx = 0, START_POINT
    area_df.loc[cy, cx] = SAND
    while True:
        for _cy, _cx in ((cy + 1, cx), (cy + 1, cx - 1), (cy + 1, cx + 1)):
            if area_df.loc[_cy, _cx] == EMPTY:
                area_df.loc[cy, cx] = EMPTY
                area_df.loc[_cy, _cx] = SAND
                cy, cx = _cy, _cx
                break
        else:
            break
    return area_df


def sand_capacity_until_abyss(xs_limits, ys_limits, rock_paths):
    area_df = _build_area(xs_limits, ys_limits, rock_paths)

    sand_units = 0
    try:
        while True:
            area_df = _handle_sand(area_df)
            sand_units += 1
    except KeyError:
        return sand_units


def sand_capacity_until_full(_, ys_limits, rock_paths):
    y_min, y_max = min(0, ys_limits[0]), (ys_limits[1] + 2)
    x_min = START_POINT - (y_max - y_min)
    x_max = START_POINT + (y_max - y_min)

    area_df = _build_area((x_min, x_max), (y_min, y_max), rock_paths)
    area_df.iloc[-1] = ROCK

    sand_units = 0
    while True:
        area_df = _handle_sand(area_df)
        sand_units += 1
        if area_df.loc[0, START_POINT] == SAND:
            return sand_units


solution_function_01 = sand_capacity_until_abyss
solution_function_02 = sand_capacity_until_full
