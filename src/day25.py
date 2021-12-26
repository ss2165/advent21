from typing import Iterator
import numpy as np
from scipy.ndimage import generic_filter



def byte_gen(s: str) -> Iterator[bytes]:
    for line in s.split("\n"):
        yield bytes(line, "utf-8")

def parse_input(path: str) -> np.ndarray:
    with open(path) as f:
        all_text = f.read()

    all_text = all_text.replace(".", "0")
    all_text = all_text.replace(">", "1")
    all_text = all_text.replace("v", "2")

    return np.genfromtxt(byte_gen(all_text), dtype=np.uint8, delimiter=1)


def draw(ar: np.ndarray) -> str:
    drawmap = {0: ".", 1: ">", 2: "v"}
    return "\n".join(("".join(map(lambda y: drawmap[y], row)) for row in ar))

def apply_filter(img: np.ndarray, left: bool) -> np.ndarray:
    footprint = np.array([[1, 1, 1]]) if left else np.array([[1], [1], [1]])
    check_val = 1 if left else 2
    def filt_func(values: np.ndarray) -> int:
        before, me, after = values
        if me == check_val and after == 0:
            return 0
        if before == check_val and me == 0:
            return before
        return me
    

    return generic_filter(img, filt_func, footprint=footprint, mode="wrap")

ar = parse_input("../inputs/day25_trial.txt")
steps = 0
while True:
    steps += 1
    print(steps)
    newar = apply_filter(ar, True)
    newar = apply_filter(newar, False)
    if (newar == ar).all():
        break

    ar = newar

print(steps)