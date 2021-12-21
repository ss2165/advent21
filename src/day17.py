from dataclasses import dataclass
import itertools
from typing import Optional

@dataclass
class Point:
    pos: int
    vel: int
    target: tuple[int, int]
    def update(self):
        return NotImplemented
    def in_target(self) -> bool:
        return self.target[0] <= self.pos <= self.target[1]
    def overshot(self) -> bool:
        return NotImplemented

@dataclass
class Xpoint(Point):
    def update(self):
        self.pos += self.vel
        if self.vel != 0:
            self.vel -= self.vel//abs(self.vel)
    def overshot(self) -> bool:
        return self.pos > self.target[1]

@dataclass
class Ypoint(Point):
    def update(self):
        self.pos += self.vel
        self.vel -= 1
    def overshot(self) -> bool:
        return self.pos < self.target[0]

def does_hit(initial: tuple[int, int], xtarget:tuple[int, int], ytarget:tuple[int, int]) -> Optional[int]:
    points = (Xpoint(0, initial[0], xtarget), Ypoint(0, initial[1], ytarget))

    step = 0
    ys = []
    while not all(p.in_target() for p in points) and not any(p.overshot() for p in points):
        ys.append(points[1].pos)
        step += 1
        _ = [p.update() for p in points]
    
    if not any(p.overshot() for p in points):
        return max(ys)
    return None


# xtarget = (20, 30)
# ytarget = (-10, -5)

xtarget = (70, 125)
ytarget = (-159, -121)

def find_big_yeet(xtarget: tuple[int, int], ytarget: tuple[int, int]) -> int:
    search = itertools.product(range(1, xtarget[1]), range(-1000, 1000))

    ymax = -1000000000
    for initial in itertools.dropwhile(lambda ini: does_hit(ini, xtarget, ytarget) is None, search):
        ym = does_hit(initial, xtarget, ytarget)
        if ym is None:
            continue

        if ym > ymax:
            ymax = ym
    return ymax


# count_hits = 0
# for x in range(1, xtarget[1]):
#     for y in range(1000, -1000):
#         if does_hit((x, y), xtarget, ytarget) is None:
#             continue
#         else: 
#             count_hits += 1

count_hits = sum(1 for x in range(1, xtarget[1]+1) for y in range(-1000, 1000) if does_hit((x, y), xtarget, ytarget) is not None)
print(count_hits)