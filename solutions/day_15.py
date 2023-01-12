# Day 15: Beacon Exclusion Zone

import pandas as pd
import re


def parse_file(fd):
    input_template = (
        r"Sensor at x=(\d+), y=(\d+): closest beacon is at x=(-?\d+), y=(\d+)"
    )
    re_pattern = re.compile(input_template, re.MULTILINE)
    coords_df = pd.DataFrame(
        [
            (re_match[1], re_match[2], re_match[3], re_match[4])
            for re_match in re_pattern.finditer(fd.read())
        ],
        columns=["sx", "sy", "bx", "by"],
    ).astype(int)
    return (coords_df,)


def find_non_beacon_places(coords_df):
    coords_df = coords_df.assign(
        d=abs(coords_df.sx - coords_df.bx) + abs(coords_df.sy - coords_df.by)
    )

    y = 2000000
    periods = []
    for _, row in coords_df.iterrows():
        if row.sy - row.d <= y and y <= row.sy + row.d:
            periods.append(
                (row.sx - (row.d - abs(row.sy - y)), row.sx + (row.d - abs(row.sy - y)))
            )
    periods = sorted(periods)

    merged_periods = []
    lp = periods[0]
    for i in range(1, len(periods)):
        if lp[1] + 1 >= periods[i][0]:
            lp = (lp[0], max(periods[i][1], lp[1]))
        else:
            merged_periods.append(lp)
            lp = periods[i]
    merged_periods.append(lp)

    return sum([f - s for s, f in merged_periods])


def calc_tuning_frequency(coords_df):
    coords_df = coords_df.assign(
        d=abs(coords_df.sx - coords_df.bx) + abs(coords_df.sy - coords_df.by)
    )
    min_coord, max_coord = 0, 4000000

    periods = [[] for _ in range(max_coord - min_coord + 1)]

    for _, row in coords_df.iterrows():
        if min_coord <= row.sy and row.sy <= max_coord:
            periods[row.sy].append(
                (max(min_coord, row.sx - row.d), min(max_coord, row.sx + row.d))
            )
        for i in range(row.d):
            period = (max(min_coord, row.sx - i), min(max_coord, row.sx + i))
            down_y = row.sy - row.d + i
            up_y = row.sy + row.d - i
            if min_coord <= down_y and down_y <= max_coord:
                periods[down_y].append(period)
            if min_coord <= up_y and up_y <= max_coord:
                periods[up_y].append(period)

    open_area = -1
    for iy, ps in enumerate(periods):
        ps = sorted(ps)
        curent_period = ps[0]
        merged_periods = []
        for ip in range(1, len(ps)):
            if curent_period[1] + 1 >= ps[ip][0]:
                curent_period = (curent_period[0], max(ps[ip][1], curent_period[1]))
            else:
                merged_periods.append(curent_period)
                curent_period = ps[ip]

        merged_periods.append(curent_period)

        if len(merged_periods) > 1:
            if open_area + 1 == iy:
                open_area += 1
            else:
                return 4000000 * (merged_periods[0][1] + 1) + iy


solution_function_01 = find_non_beacon_places
solution_function_02 = calc_tuning_frequency
