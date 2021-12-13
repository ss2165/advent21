from typing import Iterable, Optional
from collections import deque
from functools import reduce


def score_solutions(sols: Iterable[str]) -> int:
    scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    def sol_score(sol: str) -> int:
        return reduce(lambda x, y: 5 * x + y, map(scores.__getitem__, sol), 0)

    scorelist = list(map(sol_score, sols))
    scorelist.sort()
    return scorelist[int((len(scorelist) - 1) / 2)]


def stackem(line: str) -> Optional[str]:
    pairs = {"{": "}", "<": ">", "(": ")", "[": "]"}

    que = deque()
    for c in line.rstrip():
        if c in pairs:
            que.append(c)
        else:
            last_left = que.pop()
            if pairs[last_left] != c:
                return c
    return None

def stackem_close(line: str) -> str:
    pairs = {"{": "}", "<": ">", "(": ")", "[": "]"}

    que = deque()
    for c in line.rstrip():
        if c in pairs:
            que.append(c)
        else:
            _ = que.pop()

    que.reverse()
    return "".join(pairs[c] for c in que)


def part2_stack():

    with open("../inputs/day10.txt") as f2:
        incomplete = (line for line in f2.readlines() if stackem(line) is None)
        print(score_solutions(map(stackem_close, incomplete)))


def part1_stack():

    scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    with open("../inputs/day10.txt") as f2:
        corrupted = (stackem(line) for line in f2.readlines())
        corrupted = (c for c in corrupted if c is not None)

        score = sum(scores[c] for c in corrupted)
        print(score)


part1_stack()
part2_stack()


# from lark import Lark
# from lark.exceptions import UnexpectedCharacters


# def part1():

#     with open("day10.lark") as f:
#         grammar = Lark(f.read())

#     scores = {
#         ")": 3,
#         "]": 57,
#         "}": 1197,
#         ">": 25137,
#     }

#     with open("../inputs/day10.txt") as f2:
#         score = 0
#         for line in f2.readlines():
#             try:
#                 grammar.parse(line)
#             except UnexpectedCharacters as e:
#                 if e.column != len(line):
#                     score += scores[e.char]
#         print(score)


# def part2() -> list[str]:
#     charmap = {
#         "RBRACE": "}",
#         "RSQB": "]",
#         "RPAR": ")",
#         "MORETHAN": ">",
#     }

#     solution_lines = []
#     with open("../inputs/day10.txt") as f2:
#         score = 0
#         for line in f2.readlines():
#             try:
#                 grammar.parse(line)
#             except UnexpectedCharacters as e:
#                 if e.column != len(line):
#                     continue
#                 solved = False
#                 solution = ""
#                 while not solved:

#                     solution += charmap[e.allowed.intersection(charmap).pop()]
#                     try:
#                         line2 = line[:-1] + solution + line[-1]
#                         grammar.parse(line2)
#                         solved = True
#                         solution_lines.append(solution)
#                     except UnexpectedCharacters as e2:
#                         e = e2

#                 # print(e.allowed.intersection(charmap))
#                 # raise e
#         return solution_lines
