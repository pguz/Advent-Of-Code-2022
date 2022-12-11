# Day 03: Rucksack Reorganization

import pandas as pd


def parse_file(fd):
    return (pd.read_csv(fd, header=None).squeeze("columns"),)


def _sum_items_priorities(items):
    offset_uppercase_items = ord("A") - (ord("z") + 1 - ord("a")) - 1
    offset_lowercase_items = ord("a") - 1
    sum_priorities_of_uppercase_common_items = (
        items[(items >= "A") & (items <= "Z")].map(ord) - offset_uppercase_items
    ).sum()
    sum_priorities_of_lowercase_common_items = (
        items[(items >= "a") & (items <= "z")].map(ord) - offset_lowercase_items
    ).sum()
    return (
        sum_priorities_of_uppercase_common_items
        + sum_priorities_of_lowercase_common_items
    )


def sum_priorities_of_common_items(items_df):
    def find_common_item(s):
        length_by_two = len(s) // 2
        return (set(s[:length_by_two]) & set(s[length_by_two:])).pop()

    common_items = items_df.map(find_common_item)
    return _sum_items_priorities(items=common_items)


def sum_priorities_of_group_items(items_df):
    def find_group_item(group_items_series):
        group_items = group_items_series.values
        return (group_items[0] & group_items[1] & group_items[2]).pop()

    group_items = items_df.map(set).groupby(items_df.index // 3).apply(find_group_item)
    return _sum_items_priorities(items=group_items)


solution_function_01 = sum_priorities_of_common_items
solution_function_02 = sum_priorities_of_group_items
