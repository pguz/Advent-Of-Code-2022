# Day 19: Not Enough Minerals

import numpy as np
import re


def parse_file(fd):
    input_template = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    re_pattern = re.compile(input_template, re.MULTILINE)
    blueprints = [
        tuple(int(re_match[i]) for i in range(1, 8))
        for re_match in re_pattern.finditer(fd.read())
    ]
    return (blueprints,)


def _process_blueprint(blueprint, duration):
    or_or = blueprint[1]
    cl_or = blueprint[2]
    ob_or = blueprint[3]
    ob_cl = blueprint[4]
    ge_or = blueprint[5]
    ge_ob = blueprint[6]

    queue = [(0, 1, 0, 0, 0, 0, 0, 0, 0)]
    state = set()
    prev_t = 0

    def _add_cand(cand):
        if cand not in state:
            state.add(cand)
            queue.append(cand)

    def _score_func(cand):
        _, or_r, cl_r, ob_r, ge_r, or_m, cl_m, ob_m, ge_m = cand
        return (ge_m, ge_r, ob_r, ob_m, cl_r, cl_m, or_r, or_m)

    while queue:
        cur_t, or_r, cl_r, ob_r, ge_r, or_m, cl_m, ob_m, ge_m = queue.pop(0)

        if cur_t == duration:
            return max([e[8] for e in queue])

        if prev_t != cur_t:
            if cur_t >= 16:
                rank = sorted(
                    [(_score_func(cand), cand) for cand in queue], reverse=True
                )
                queue = [cand for _, cand in rank[: len(rank) // 4]]

            state = set()
            prev_t = cur_t

        cur_t += 1
        or_n = or_m + or_r
        cl_n = cl_m + cl_r
        ob_n = ob_m + ob_r
        ge_n = ge_m + ge_r

        _add_cand((cur_t, or_r, cl_r, ob_r, ge_r, or_n, cl_n, ob_n, ge_n))

        if or_or <= or_m:
            _add_cand(
                (cur_t, or_r + 1, cl_r, ob_r, ge_r, or_n - or_or, cl_n, ob_n, ge_n)
            )

        if cl_or <= or_m:
            _add_cand(
                (cur_t, or_r, cl_r + 1, ob_r, ge_r, or_n - cl_or, cl_n, ob_n, ge_n)
            )

        if ob_or <= or_m and ob_cl <= cl_m:
            _add_cand(
                (
                    cur_t,
                    or_r,
                    cl_r,
                    ob_r + 1,
                    ge_r,
                    or_n - ob_or,
                    cl_n - ob_cl,
                    ob_n,
                    ge_n,
                )
            )

        if ge_or <= or_m and ge_ob <= ob_m:
            _add_cand(
                (
                    cur_t,
                    or_r,
                    cl_r,
                    ob_r,
                    ge_r + 1,
                    or_n - ge_or,
                    cl_n,
                    ob_n - ge_ob,
                    ge_n,
                )
            )


def calc_quality_level(blueprints):
    return sum(
        [
            i * _process_blueprint(blueprint, 24)
            for i, blueprint in enumerate(blueprints, start=1)
        ]
    )


def geodes_after_32_min(blueprints):
    return np.prod([_process_blueprint(blueprint, 32) for blueprint in blueprints[:3]])


solution_function_01 = calc_quality_level
solution_function_02 = geodes_after_32_min
