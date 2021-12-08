from dataclasses import dataclass
from typing import Iterable, Iterator


@dataclass
class OneLine:
    code: set[str]
    msg: list[str]


def alphabetise(inp: str) -> str:
    return "".join(sorted(inp))


def parse_input(path: str) -> list[OneLine]:
    with open(path) as f:
        lines = f.readlines()

    outs = []

    for line in lines:
        line = line.rstrip()
        codes, msg = line.split(" | ", 2)
        outs.append(
            OneLine(
                set(alphabetise(code) for code in codes.split(" ")),
                list(map(alphabetise, msg.split(" "))),
            )
        )

    return outs


def count_easy(inp: list[OneLine]) -> int:
    filtered = [msg for ol in inp[:1] for msg in ol.msg if len(msg) in (2, 4, 3, 7)]
    print(filtered)
    return len(filtered)


def find_len(code: set[str], leng: int) -> Iterator[str]:
    return (wor for wor in code if len(wor) == leng)


def diffset(word: str, other: str) -> set[str]:
    return set(list(word)) - set(list(other))

def symdifffset(word: str, other: str) -> set[str]:
    return set(list(word)) ^ set(list(other))

def interset(word: str, other: str) -> set[str]:
    return set(list(word)) & set(list(other))

def get_only(words: set[str]) -> str:
    assert len(words) == 1
    return words.pop()

def code_from_letters(letters: Iterable[str]) -> str:
    return "".join(sorted(letters))

def decode(code: set[str]) -> dict[str, int]:
    known_lengths = ((1, 2), (4, 4), (7, 3), (8, 7))

    rev_encoding = {}
    letter_map: dict[str, str] = {}
    # code_sets = set(set(list(word)) for word in code)
    for dig, leng in known_lengths:
        code_word = next(find_len(code, leng))
        code.remove(code_word)
        rev_encoding[dig] = code_word

    letter_map["a"] = get_only(diffset(rev_encoding[7], rev_encoding[1]))
    bd_set = diffset(rev_encoding[4], rev_encoding[7])

    len_five_words = set(find_len(code, 5))

    letter_map["d"] = next(
        letter for letter in bd_set if all(letter in word for word in len_five_words)
    )
    bd_set.remove(letter_map["d"])
    letter_map["b"] = get_only(bd_set)

    rev_encoding[5] = next(word for word in len_five_words if letter_map["b"] in word)
    len_five_words.remove(rev_encoding[5])

    two_and_three = list(len_five_words)
    ef_set = symdifffset(*two_and_three)

    letter_map["f"] = get_only(interset(rev_encoding[5], "".join(ef_set)))

    ef_set.remove(letter_map["f"])
    letter_map["e"] = get_only(ef_set)

    rev_encoding[2] = next(word for word in len_five_words if letter_map["e"] in word)
    in_two_not_five = diffset(rev_encoding[2], rev_encoding[5])
    in_two_not_five.remove(letter_map["e"])
    letter_map["c"] = get_only(in_two_not_five)
    letter_map["g"] = get_only(diffset(rev_encoding[8], "".join(letter_map.values())))


    rev_encoding[0] = code_from_letters((letter_map[l] for l in "abcefg"))
    rev_encoding[3] = code_from_letters((letter_map[l] for l in "acdfg"))
    rev_encoding[6] = code_from_letters((letter_map[l] for l in "abdefg"))
    rev_encoding[9] = code_from_letters((letter_map[l] for l in "abcdfg"))

    return {val: key for key, val in rev_encoding.items()}


def decode_line(line: OneLine) -> int:
    encoding = decode(line.code)
    return int("".join(map(str, (encoding[msg] for msg in line.msg))))


inp = parse_input("../inputs/day8.txt")

print(sum(decode_line(line) for line in inp))
