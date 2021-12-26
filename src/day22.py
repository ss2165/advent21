from typing import Iterator
from dataclasses import dataclass
import numpy as np
import operator
import itertools
from functools import reduce


def parse_input(path: str) -> Iterator[tuple[bool, np.ndarray]]:
    with open(path) as f:
        for line in f:
            state, rest = line.rstrip().split(" ")
            coords = np.array(
                [[int(n) for n in s[2:].split("..")] for s in rest.split(",")]
            )
            coords[:, 1] += 1
            yield (state == "on", coords)


def part1():
    cubes = np.zeros((101, 101, 101), dtype=bool)

    for state, coords in parse_input("../inputs/day22.txt"):
        coords += 50

        if (coords[:, 0] >= 0).all() and (coords[:, 1] <= 101).all():
            cubes[
                coords[0, 0] : coords[0, 1],
                coords[1, 0] : coords[1, 1],
                coords[2, 0] : coords[2, 1],
            ] = state

    print(np.count_nonzero(cubes))


@dataclass(unsafe_hash=True)
class Cuboid:
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @property
    def coords(self) -> list[tuple[int, int]]:
        return [self.x, self.y, self.z]

    def volume(self) -> int:
        return reduce(operator.mul, map(lambda a: a[1] - a[0], self.coords))

    def no_volume(self) -> bool:
        return any(x[1] == x[0] for x in self.coords)

    def intersects(self, other: "Cuboid") -> bool:
        return all(
            me[0] < he[1] and he[0] < me[1] for me, he in zip(self.coords, other.coords)
        )

    def intersection(self, other: "Cuboid") -> "Cuboid":
        bounds = (
            (max(me[0], he[0]), min(me[1], he[1]))
            for me, he in zip(self.coords, other.coords)
        )

        return Cuboid(*bounds)

    def extension(self, other: "Cuboid") -> bool:
        if self.x[1] == other.x[0] and self.y == other.y and self.z == other.z:
            self.x = (self.x[0], other.x[1])
            return True

        if self.x[0] == other.x[1] and self.y == other.y and self.z == other.z:
            self.x = (other.x[0], self.x[1])
            return True

        if self.y[1] == other.y[0] and self.x == other.x and self.z == other.z:
            self.y = (self.y[0], other.y[1])
            return True

        if self.y[0] == other.y[1] and self.x == other.x and self.z == other.z:
            self.y = (other.y[0], self.y[1])
            return True

        if self.z[1] == other.z[0] and self.x == other.x and self.y == other.y:
            self.z = (self.z[0], other.z[1])
            return True

        if self.z[0] == other.z[1] and self.x == other.x and self.y == other.y:
            self.z = (other.z[0], self.z[1])
            return True

        return False

    def shatter(self, fragment: "Cuboid") -> set["Cuboid"]:
        marks = [
            [sel[0], frag[0], frag[1], sel[1]]
            for sel, frag in zip(self.coords, fragment.coords)
        ]

        ranges = [
            [(mark[i], mark[i + 1]) for i in range(len(mark) - 1)] for mark in marks
        ]
        xslice1 = Cuboid(ranges[0][0], self.y, self.z)
        xslice2 = Cuboid(ranges[0][2], self.y, self.z)

        yslice1 = Cuboid(fragment.x, ranges[1][0], self.z)
        yslice2 = Cuboid(fragment.x, ranges[1][2], self.z)

        zslice1 = Cuboid(fragment.x, fragment.y, ranges[2][0])
        zslice2 = Cuboid(fragment.x, fragment.y, ranges[2][2])
        return set(
            cb
            for cb in (xslice1, xslice2, yslice1, yslice2, zslice1, zslice2)
            if not cb.no_volume()
        )


@dataclass
class Reactor:
    cuboids: set[Cuboid]

    def turn_off(self, cub: Cuboid):
        new_set = set()
        for sel_c in self.cuboids:
            if not sel_c.intersects(cub):
                new_set.add(sel_c)
                continue
            intersection = sel_c.intersection(cub)
            frags = sel_c.shatter(intersection)
            new_set.update(frags)
        self.cuboids = new_set

    def turn_on(self, cub: Cuboid):
        to_add = {cub}
        while to_add:
            candidate = to_add.pop()
            try:
                intersector = next(c for c in self.cuboids if c.intersects(candidate))
                intersection = intersector.intersection(candidate)
                frags = candidate.shatter(intersection)
                to_add.update(frags)
            except StopIteration:
                self.cuboids.add(candidate)

    def number_on(self) -> int:
        return sum(c.volume() for c in self.cuboids)


def test_cuboid():
    c1 = Cuboid((0, 2), (0, 2), (0, 2))
    assert c1.volume() == 8

    c2 = Cuboid((1, 2), (1, 2), (0, 2))
    assert c2.volume() == 2

    assert c1.intersects(c2)

    assert c1.intersection(c2) == c2
    shattered = c1.shatter(c2)
    assert len(shattered) == 2

    assert not any(c.intersects(c2) for c in shattered)
    c4 = Cuboid((1, 2), (1, 2), (0, 3))
    assert c1.intersection(c4) == c2

    c3 = Cuboid((2, 3), (2, 3), (2, 3))

    assert not c1.intersects(c3)

    c5 = Cuboid((0, 1), (0, 1), (0, 1))
    c6 = Cuboid((0, 1), (0, 1), (1, 2))

    assert c5.volume() == 1
    assert c5.extension(c6)
    assert c5.volume() == 2


def test_reactor():
    rec = Reactor({Cuboid((-2, 0), (-2, 0), (-2, 0))})

    rec.turn_off(Cuboid((-2, -1), (-2, -1), (-2, 0)))

    assert rec.number_on() == 6

    rec.turn_on(Cuboid((0, 2), (0, 2), (0, 2)))
    assert rec.number_on() == 14


def part2():
    rec = Reactor(set())
    i = 0
    for state, coords in parse_input("../inputs/day22.txt"):
        i += 1
        print(i)
        if not ((coords[:, 0] >= -50).all() and (coords[:, 1] <= 50).all()):
            continue
        cub = Cuboid(*(tuple(row) for row in coords))
        rec.turn_on(cub) if state else rec.turn_off(cub)
    print(len(rec.cuboids))
    print(rec.number_on())


if __name__ == "__main__":
    part2()
