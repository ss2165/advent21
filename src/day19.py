from typing import Iterator, Optional
import numpy as np
import itertools


import itertools as it

rot_mats = np.loadtxt("day19_matrices.txt", dtype=int).reshape((-1, 3, 3))


def parse_input(path: str, dimensions: int = 3) -> list[np.ndarray]:
    with open(path) as f:
        txt = f.read()

    ar_txts = txt.split("\n\n")
    return [
        np.fromstring(
            ar[ar.index("\n") + 1 :].replace("\n", ","), dtype=int, sep=","
        ).reshape((-1, dimensions))
        for ar in ar_txts
    ]


def all_rots(scan: np.ndarray) -> Iterator[np.ndarray]:
    for mat in rot_mats:
        yield np.dot(mat, scan.T).T


def test_rots():
    scans = parse_input("../inputs/day19_rots.txt", 3)
    onerots = list(all_rots(scans[0]))
    for m in scans:
        assert any((m == m2).all() for m2 in onerots)


def compare_slices(
    p1: np.ndarray, p2: np.ndarray, axis: int = 0, n_points: int = 12
) -> Optional[np.ndarray]:
    slice1 = p1[np.argsort(p1[:, axis])[:n_points]]
    slice2 = p2[np.argsort(p1[:, axis])[-n_points:]]
    diff = slice2[0] - slice1[0]
    print(diff)
    slice1 += diff
    if (slice1 == slice2).all():
        return diff
    return None


def find_diff(
    ar1: np.ndarray, ar2: np.ndarray
) -> Optional[tuple[np.ndarray, np.ndarray]]:

    for _, s2 in enumerate(all_rots(ar2)):
        for i, j in itertools.product(
            range(ar1.shape[0] - 12), range(s2.shape[0] - 12)
        ):
            p1, p2 = ar1[i], s2[j]
            diff = p2 - p1
            ar1comp = s2 - diff
            if np.count_nonzero((ar1[:, None] == ar1comp).all(-1).any(1)) == 12:
                return ar1comp, diff
    return None


# scans = parse_input("../inputs/day19_trial.txt")
scans = parse_input("../inputs/day19.txt")
n_scanners = len(scans)
found_scanners = [0]
scanner_pos = np.zeros((n_scanners, 3), dtype=int)
while len(found_scanners) != n_scanners:
    print(len(found_scanners))
    to_find = filter(lambda x: x not in found_scanners, range(n_scanners))
    for current_scanner, other_scanner in itertools.product(
        reversed(found_scanners), to_find
    ):
        if (ret := find_diff(scans[current_scanner], scans[other_scanner])) is not None:
            new_other, diff = ret
            scanner_pos[other_scanner] = diff
            found_scanners.append(other_scanner)
            scans[other_scanner] = new_other
            break

unique_points = np.unique(np.vstack(scans), axis=0)
print(len(unique_points))
print(scanner_pos)
print(max(np.abs(s2 - s1).sum() for s1, s2 in itertools.combinations(scanner_pos, 2)))
