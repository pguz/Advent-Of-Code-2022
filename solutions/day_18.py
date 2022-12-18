# Day 18: Boiling Boulders

import pandas as pd


def parse_file(fd):
    droplets = pd.read_csv(fd, header=None)
    return (droplets,)


def calc_lava_surface_area(droplets):
    coords = set(droplets.columns)
    return 6 * len(droplets) - 2 * sum(
        [
            droplets.sort_values(by=[z])
            .groupby(base, group_keys=False)[z]
            .apply(pd.Series.diff)
            .map(lambda c: c == 1)
            .sum()
            .sum()
            for z in coords
            if (base := list(coords - {z}))
        ]
    )


def calc_exterior_lava_surface_area(droplets):
    whole_area = {
        (x, y, z)
        for x in range(droplets[0].min(), droplets[0].max() + 1)
        for y in range(droplets[1].min(), droplets[1].max() + 1)
        for z in range(droplets[2].min(), droplets[2].max() + 1)
    }
    droplet_cubes = {tuple(droplet_cube) for droplet_cube in droplets.values}
    trapped_cubes_cands = whole_area - droplet_cubes

    trapped_cubes = set()
    while trapped_cubes_cands:
        trapped_area_origin = trapped_cubes_cands.pop()
        trapped_area_stack = {trapped_area_origin}
        trapped_area_processed = {trapped_area_origin}
        trapped_area = True
        while trapped_area_stack:
            cand = trapped_area_stack.pop()
            for neigh in [
                (cand[0] - 1, cand[1], cand[2]),
                (cand[0] + 1, cand[1], cand[2]),
                (cand[0], cand[1] - 1, cand[2]),
                (cand[0], cand[1] + 1, cand[2]),
                (cand[0], cand[1], cand[2] - 1),
                (cand[0], cand[1], cand[2] + 1),
            ]:
                if neigh in trapped_area_processed:
                    continue
                if neigh in trapped_cubes_cands:
                    trapped_cubes_cands.remove(neigh)
                    trapped_area_stack.add(neigh)
                    trapped_area_processed.add(neigh)
                elif neigh not in droplet_cubes:
                    trapped_area = False
        if trapped_area:
            trapped_cubes.update(trapped_area_processed)

    return calc_lava_surface_area(droplets) - calc_lava_surface_area(
        pd.DataFrame(trapped_cubes)
    )


solution_function_01 = calc_lava_surface_area
solution_function_02 = calc_exterior_lava_surface_area
