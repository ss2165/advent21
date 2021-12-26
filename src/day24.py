import itertools
import operator
from typing import Callable
from sympy import (
    symbols,
    Piecewise,
    Abs,
    solveset,
    solve,
    Ne,
    Predicate,
    Integer,
    Q,
    refine,
    ask,
)
from sympy.solvers.inequalities import *
from sympy.solvers.solveset import nonlinsolve
import numpy as np

class DigitPredicate(Predicate):
    name = "digit"


Q.digit = DigitPredicate()


@Q.digit.register(Integer)
def _(int1, assumptions):
    return 1 <= int1 <= 9


class NeqPredicate(Predicate):
    name = "neq"


Q.neq = NeqPredicate()


@Q.neq.register(Integer, Integer)
def _(int1, int2, assumptions):
    return int1 != int2


def parse_input():
    with open("../inputs/day24.txt") as f:
        monad = f.read()
        segs = monad.split("inp w")[1:]
        segs = [l.split("\n") for l in segs]
        for lines in zip(*segs):
            # print(lines)
            if not len(set(lines)) == 1:
                # print(lines)
                yield [int(s.split(" ")[-1]) for s in lines]
        # for s in monad.split("inp w"):
        #     print(s)


def run_monad(input: str) -> int:
    innums = (int(c) for c in input)

    var = dict.fromkeys("xyzw", 0)

    def apply_op(op: str, v1: str, v2: str):
        opmap = {
            "add": operator.add,
            "mul": operator.mul,
            "div": operator.floordiv,
            "mod": operator.mod,
            "eql": operator.eq,
        }
        arg = var[v2] if v2 in var else int(v2)
        var[v1] = int(opmap[op](var[v1], arg))

    with open("../inputs/day24.txt") as f:
        for line in f:
            line = line.rstrip()
            if line == "inp w":
                var["w"] = next(innums)
            else:
                apply_op(*line.split(" "))

    return var["z"]


al, bl, cl = parse_input()


def gen_f(a: int, b: int, c: int) -> Callable[[int, int], int]:
    def f(w: int, z: int) -> int:
        gam = int(((z % 26) + b) != w)
        return (z // a) * (25 * gam + 1) + gam * (w + c)

    return f


def analytic_monad(input: str, its: int = 14) -> int:
    # innums = (int(c) for c in str(input))
    innums = (int(c) for c in input)
    z = 0
    it = 0
    for a, b, c in zip(al, bl, cl):
        if it == its:
            break
        it += 1
        w = next(innums)
        z = gen_f(a, b, c)(w, z)
    return z


def sym_solve():
    ws = symbols(" ".join(f"w{i}" for i in range(2)), integer=True)
    z = 0
    eqs = []
    for w, a, b, c in zip(ws, al, bl, cl):
        gam = (z % 26) + b
        # print(solveset(reduce_abs_inequalities([(gam, ">"), (w, ">"), (w - 10,
        # "<")], w), w))
        # print(solve([Ne(gam, w), w > 0, w - 10 < 0], [w]))
        print(ask(Q.neq(gam, w), Q.digit(w)))
        z = Piecewise(
            (
                26 * (z // a) + w + c,
                reduce_abs_inequalities([(gam, ">"), (w, ">"), (w - 10, "<")], w),
            ),
            ((z // a), True),
        )
        # z = reduce_abs_inequality
    print(z)


# sym_solve()

# target = 0
# for dig_i in range(1, 14):
#     a, b, c = list(zip(al, bl, cl))[-dig_i]
#     f = gen_f(a, b, c)

#     for thing in ((z, i) for z in range(1000000) for i in range(9, 0, -1) if (g:=f(i, z)) ==target):
#        target,j_ = thing
#        print(thing)
#        break

a, b, c = list(zip(al, bl, cl))[0]
for i, (a, b, c) in enumerate(list(zip(al, bl, cl))):
    print(i, a, b, c)
f = gen_f(a, b, c)

print(
    set(
        ((676 * w0 + 26 * w1 + w2 + 2349) //26)% 26 - 4
        for w0, w1, w2 in itertools.product(range(1, 10), range(1, 10), range(1, 10))
    )
)



# for thing in ((z, j) for z in range(100) for j in range(9, 0, -1) if (g:=f(j, z)) ==16):
#     target,j_ = thing
#     print(thing)


digs = [9] * 9 + [5, 9, 9, 9, 9]


def replace_i(dugs: list[int], index: int, val: int) -> str:
    dugs[index] = val
    return "".join(map(str, dugs))


# for _ in range(1000):
#     for dig_i in range(9):
#         min_i = min(((run_monad(replace_i(digs, dig_i, trial)), trial) for trial in range(9, 0, -1)), key=lambda x: x[0])
#         digs[dig_i] = min_i[1]
# print(min_i)

for i, randint in enumerate(np.random.randint(1, 10, (1000, 14))):
    if randint[2] > 6:
        continue
    randint[3] = randint[2] + 3
    if randint[4] < 7:
        continue
    randint[5] = randint[4] - 6

    randint[1] = 1
    randint[6] = 9

    if randint[9] < 6:
        continue
    randint[10] = randint[9] - 5

    if randint[8] >8:
        continue
    randint[11] = randint[8] + 1

    if randint[7] > 4:
        continue
    randint[12] = randint[7] + 5

    if randint[0] < 5:
        continue
    randint[13] = randint[0] - 4

    randstr = "".join(chr(48+i) for i in randint)
    z3 = analytic_monad(randstr, 3)
    z1_calc = randint[0] + 3
    z2_calc = 26*randint[0] + randint[1] + 90
    z3_calc = 676*randint[0] + 26*randint[1] + randint[2] + 2349
    z4_calc = z3_calc // 26

    z7_calc = randint[0] + 3
    z7 = analytic_monad(randstr, 7)

    c1 = analytic_monad(randstr, 11)
    c2 = analytic_monad(randstr, 9)
    # if c1 !=c2:
    #     print("oh no", i)
    #     print(c1, c2)

    print(randstr, analytic_monad(randstr))

print(run_monad("91699394894995"))
print(run_monad("51147191161261"))
# trial = 99999999
# done = False
# while not done:
#     if analytic_monad(int(str(trial) + "599999")) == 0:
#         break
#     trial -= 1
#     print(trial*100/99999999)
