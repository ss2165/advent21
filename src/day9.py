import numpy as np
import itertools

inpar = np.genfromtxt("../inputs/day9.txt", delimiter=1, dtype=int)


def neighs(i: int, bound: int) -> list[int]:
    x_neigs = []
    if i != 0:
        x_neigs.append(i - 1)
    if i != bound - 1:
        x_neigs.append(i + 1)

    return x_neigs


def find_lows(ar: np.ndarray) -> list[tuple[int, int]]:
    wid, hei = ar.shape
    return [
        (i, j)
        for i, j in itertools.product(range(wid), range(hei))
        if all(ar[i, j] < ar[i2, j] for i2 in neighs(i, wid))
        and all(ar[i, j] < ar[i, j2] for j2 in neighs(j, hei))
    ]


def find_score(ar: np.ndarray) -> int:
    indices = tuple(zip(*find_lows(ar)))
    ar[indices] += 1
    return np.sum(ar[indices])


def find_basins_distance(ar: np.ndarray):
    lows = find_lows(ar)
    wid, hei = ar.shape
    low_sizes = [0] * len(lows)
    for i, j in itertools.product(range(wid), range(hei)):
        if ar[i, j] == 9:
            continue
        dists = [(i2 - i) ** 2 + (j2 - j) ** 2 for i2, j2 in lows]
        closest_low = dists.index(min(dists))
        low_sizes[closest_low] += 1

    return low_sizes


def find_basin(ar: np.ndarray, low: tuple[int, int]) -> set[tuple[int, int]]:
    boundary = set([low])
    done = False
    wid, hei = ar.shape
    basin = set()
    while not done:
        new_boundary = set()
        for i, j in boundary:
            nes = [(i2, j) for i2 in neighs(i, wid)]
            nes += [(i, j2) for j2 in neighs(j, hei)]

            new_boundary.update(
                ne
                for ne in nes
                if ar[ne] != 9 and ar[ne] > ar[i, j] and ne not in basin
            )
        if len(new_boundary) == 0:
            done = True
        basin.update(boundary)
        boundary = new_boundary
    return basin


def find_n_basins(ar: np.ndarray) -> list[int]:
    lows = find_lows(ar)
    top3_basin_sizes = []
    for low in lows:
        basin = find_basin(ar, low)
        size = len(basin)
        if len(top3_basin_sizes) < 3:
            top3_basin_sizes.append(size)
            top3_basin_sizes.sort()

        else:
            if size > top3_basin_sizes[0]:
                top3_basin_sizes.insert(1, size)
                top3_basin_sizes = top3_basin_sizes[1:]
                top3_basin_sizes.sort()
    return top3_basin_sizes



top_bas = find_n_basins(inpar)
print(top_bas)
import operator
from functools import reduce

print(reduce(operator.mul, top_bas))
