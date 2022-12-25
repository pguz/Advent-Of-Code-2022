# Day 25: Full of Hot Air

import pandas as pd


def parse_file(fd):
    return (pd.read_csv(fd, header=None).squeeze("columns"),)


def _from_snafu(snafu):
    con = {
        "=": -2,
        "-": -1,
        "0": 0,
        "1": 1,
        "2": 2,
    }
    return sum([con[v] * pow(5, i) for i, v in enumerate(snafu[::-1])])


def _to_snafu(number):
    con = {
        0: "0",
        1: "1",
        2: "2",
        3: "=",
        4: "-",
    }
    snafu = ""
    while number:
        q, r = divmod(number, 5)
        snafu = con[r] + snafu
        number = q + 1 if r > 2 else q
    return snafu


def calc_snafu(snafu_numbers):
    return _to_snafu(snafu_numbers.map(_from_snafu).sum())


solution_function_01 = calc_snafu
solution_function_02 = None
