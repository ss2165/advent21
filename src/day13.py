from functools import reduce
import numpy as np
from itertools import takewhile


def parse_input(path: str) -> tuple[np.ndarray, list[tuple[str, int]]]:
    pref = len("fold along ")
    with open(path) as f:
        lines = iter(f.readlines())
    points = takewhile(lambda x: len(x) > 1, lines)

    xy = (tuple(map(int, p.rstrip().split(","))) for p in points)

    x, y = zip(*xy)

    insts = (l[pref:].split("=") for l in lines)
    inst_lines = [(ins[0], int(ins[1])) for ins in insts]

    ar = np.zeros((max(x) + 1, max(y) + 1), dtype=bool)
    ar[(x, y)] = True
    return ar, inst_lines


def draw(ar: np.ndarray) -> str:
    return "\n".join(("".join(map(lambda y: "#" if y else " ", row)) for row in ar.T))


def x_fold(arx: np.ndarray, val: int) -> np.ndarray:
    ar1 = arx[:val, :]
    ar2 = arx[val + 1 :, :]
    ar2 = np.flipud(ar2)
    diff = ar1.shape[0] - ar2.shape[0]
    ar1[diff:, :] |= ar2
    return ar1


def fold(ar: np.ndarray, inst: tuple[str, int]) -> np.ndarray:
    match inst:
        case ("x", x):
            return x_fold(ar, x)
        case ("y", y):
            return x_fold(ar.T, y).T

    return ar


inar, folds = parse_input("../inputs/day13.txt")
folded = reduce(fold, folds, inar)

print(draw(folded))
# print(np.count_nonzero(newar))
