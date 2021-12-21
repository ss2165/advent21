import numpy as np
import scipy.ndimage as ndimage

NEIGHBOUR_KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)


def update_ar(ar: np.ndarray) -> int:
    flashed_mask = np.zeros_like(ar, dtype=bool)
    ar += 1
    while True:
        newflashes = ar > 9
        if np.count_nonzero(newflashes) == 0:
            break
        flashed_mask |= newflashes
        incr = ndimage.convolve(
            newflashes.astype(int), NEIGHBOUR_KERNEL, mode="constant"
        )
        ar[~flashed_mask] += incr[~flashed_mask]
        ar[newflashes] = 0

    return np.count_nonzero(flashed_mask)


def flashes(ar: np.ndarray, steps: int) -> int:
    return sum(update_ar(ar) for _ in range(steps))


def first_full_flash(ar: np.ndarray) -> int:
    step = 1
    while update_ar(ar) != ar.size:
        step += 1

    return step


inpar = np.genfromtxt("../inputs/day11.txt", delimiter=1, dtype=int)

print(flashes(inpar.copy(), 100))
print(first_full_flash(inpar))
