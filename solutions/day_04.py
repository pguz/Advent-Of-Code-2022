# Day 04: Camp Cleanup

import pandas as pd


def parse_file(fd):
    return (pd.read_csv(fd, header=None, engine="python", delimiter=",|-"),)


def count_fully_overlapping(input_df):
    first_contains_second = (input_df[0] <= input_df[2]) & (input_df[3] <= input_df[1])
    second_contains_first = (input_df[2] <= input_df[0]) & (input_df[1] <= input_df[3])
    return (first_contains_second | second_contains_first).sum()


def count_overlapping(input_df):
    first_case_not_overlapping = input_df[1] < input_df[2]
    second_case_not_overlapping = input_df[3] < input_df[0]
    return len(input_df[~(first_case_not_overlapping | second_case_not_overlapping)])


solution_function_01 = count_fully_overlapping
solution_function_02 = count_overlapping
