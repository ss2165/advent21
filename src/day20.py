from os import sep
from typing import Iterator
import numpy as np
from numpy.lib.function_base import quantile
from scipy.ndimage import generic_filter
import imageio
def byte_gen(s: str) -> Iterator[bytes]:
    for line in s.split("\n"):
        yield bytes(line, "utf-8")

def draw(ar: np.ndarray) -> str:
    return "\n".join(("".join(map(lambda y: "#" if y else ".", row)) for row in ar))

def parse_input(path: str) -> tuple[np.ndarray, np.ndarray]:
    with open(path) as f:
        all_text = f.read()

    all_text = all_text.replace("#", "1")
    all_text = all_text.replace(".", "0")

    l2, rest = all_text.split("\n\n")
    return np.genfromtxt(byte_gen(l2), dtype=np.uint8, delimiter=1), np.genfromtxt(
        byte_gen(rest), dtype=np.uint8, delimiter=1
    )
    # print(np.frombuffer(bytes(l2, "ascii"), dtype=bool))



def apply_filter(img: np.ndarray, code: np.ndarray, pad: int) -> np.ndarray:
    padding = np.uint8(pad)
    padded = np.pad(img, ((1, 1), (1, 1)), mode="constant", constant_values=padding)
    def filt_func(values: np.ndarray) -> int:
        index = int("".join(map(str, map(int, values))), 2)
        return code[index]
    

    return generic_filter(padded, filt_func, size=(3, 3), mode="constant", cval=padding)

# code, img = parse_input("../inputs/day20_trial.txt")
code, img = parse_input("../inputs/day20.txt")



for i in range(50):
    img = apply_filter(img, code, i%2 if code[0] else 0)

# print(draw(img))
imageio.imwrite('img_saved.jpg', img.astype(float))
# print(np.count_nonzero(img))