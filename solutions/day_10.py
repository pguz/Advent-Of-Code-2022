# Day 10: Cathode-Ray Tube

import numpy as np
import pandas as pd


def parse_file(fd):
    instructions = pd.read_csv(fd, header=None, delimiter=" ", names=["inst", "value"])
    instructs_effective_cycles = (instructions["value"].notnull() + 1).cumsum()
    instructs_schedule = instructions["value"].rename(index=instructs_effective_cycles)
    cpu_schedule = instructs_schedule.combine_first(
        pd.Series(np.zeros(instructs_effective_cycles.iloc[-1]))
    )
    cpu_schedule[0] = 1
    return (cpu_schedule,)


def sum_of_signal_strengths(cpu_schedule):
    signal_strength_cycles = cpu_schedule.cumsum().shift(1)[
        cpu_schedule.index % 40 == 20
    ]
    sum_signal_strengths = (
        signal_strength_cycles.reset_index()
        .apply(lambda r: r["index"] * r["value"], axis=1)
        .sum()
    )
    return sum_signal_strengths


def print_crt(cpu_schedule):
    def set_pixels(cycles):
        return ((cycles["index"] % 40) - cycles["value"]).abs() <= 1

    crt = (
        cpu_schedule.cumsum()
        .reset_index()
        .pipe(set_pixels)
        .map({True: "#", False: "."})
    )
    crt_rows = crt.groupby(cpu_schedule.index // 40).apply("".join)
    return crt_rows.map(lambda s: s.count("#")).sum()


solution_function_01 = sum_of_signal_strengths
solution_function_02 = print_crt
