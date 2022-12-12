# Day 12: Hill Climbing Algorithm

import pandas as pd
import numpy as np


def parse_file(fd):
    input_area = pd.read_csv(fd, header=None).squeeze("columns")
    return (pd.DataFrame(list(input_area.map(list))),)


def _steps_to_the_best_location(area_df, start_point):
    sources = (
        area_df[area_df == start_point]
        .dropna(axis=1, how="all")
        .dropna(how="all")
        .stack()
        .index.tolist()
    )
    destination = area_df[area_df == "E"].dropna(axis=1, how="all").dropna(how="all")
    j_dest, i_dest = destination.index.item(), destination.columns.item()

    area_df[area_df == "S"] = "a"
    area_df[area_df == "E"] = "z"
    area_df = pd.DataFrame(np.vectorize(ord)(area_df))

    height, width = area_df.shape
    area = area_df.values.tolist()
    visited = set(sources)
    queue = [(j_src, i_src, 0) for j_src, i_src in sources]

    def _handle_cell(i_, j_):
        if (j_, i_) not in visited and area[j_][i_] <= area[j][i] + 1:
            queue.append((j_, i_, l + 1))
            visited.add((j_, i_))

    while queue:
        j, i, l = queue.pop(0)
        if i == i_dest and j == j_dest:
            return l

        if j > 0:
            _handle_cell(i, j - 1)
        if i > 0:
            _handle_cell(i - 1, j)
        if j < height - 1:
            _handle_cell(i, j + 1)
        if i < width - 1:
            _handle_cell(i + 1, j)


def steps_to_the_best_location_from_S(area):
    return _steps_to_the_best_location(area, start_point="S")


def steps_to_the_best_location_from_a(area):
    area[area == "S"] = "a"
    return _steps_to_the_best_location(area, start_point="a")


solution_function_01 = steps_to_the_best_location_from_S
solution_function_02 = steps_to_the_best_location_from_a
