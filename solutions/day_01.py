# Day 01: Calorie Counting

import numpy as np
import pandas as pd


def parse_file(fd):
    return (pd.read_csv(fd, header=None, skip_blank_lines=False).squeeze("columns"),)


def count_calories(calories):
    return int(calories.groupby(np.isnan(calories).cumsum()).sum().max())


def count_calories_top3(calories):
    return int(calories.groupby(np.isnan(calories).cumsum()).sum().nlargest(3).sum())


solution_function_01 = count_calories
solution_function_02 = count_calories_top3
