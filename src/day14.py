from collections import Counter


def parse_input(path: str) -> tuple[str, dict[str, str]]:
    with open(path) as f:
        lines = f.readlines()
    init = lines[0].rstrip()
    rules = dict(l.rstrip().split(" -> ") for l in lines[2:])
    return init, rules


def counter(start: str) -> Counter[str]:
    return Counter(start[i : i + 2] for i in range(len(start) - 1))


def apply_rules(start: str) -> str:
    # bad, exponential solution
    inserts = [rules.get(start[i : i + 2], "") for i in range(len(start) - 1)] + [""]
    return "".join(v for pair in zip(start, inserts) for v in pair)


def update_counter(counter: Counter[str], rules: dict[str, str]) -> Counter[str]:
    newcounter = Counter()
    for st, count in counter.items():
        newcounter[st[0] + rules[st]] += count
        newcounter[rules[st] + st[1]] += count
    return newcounter


def score_counter(counter: Counter[str]) -> int:
    letter_count = Counter()
    for pair, count in counter.items():
        letter_count[pair[0]] += count
    stats = letter_count.most_common()
    return stats[0][1] - stats[-1][1]


init, rules = parse_input("../inputs/day14.txt")
trail_letter = init[-1]

cinit = counter(init)
for _ in range(40):
    cinit = update_counter(cinit, rules)

cinit[trail_letter] += 1
print(score_counter(cinit))
