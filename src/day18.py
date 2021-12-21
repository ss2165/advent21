from dataclasses import dataclass
from typing import Callable, Iterable, Iterator, Optional, Union, TypeAlias
from ast import literal_eval
import pytest
from functools import reduce
import operator
import itertools
from copy import deepcopy
PairList = list[Union[int, "PairList"]]
Node: TypeAlias = Union[int, "Pair"]

@dataclass
class Pair:
    left: Node
    right: Node
    
    @classmethod
    def from_list(cls, lst: PairList):
        l, r = lst
        
        return Pair(parse_x(l), parse_x(r))
    

    def __add__(self, other: "Pair") -> "Pair":
        out = Pair(deepcopy(self), deepcopy(other))
        out.reduce()
        return out
    
    def reduce(self):
        done = False
        while not done:
            while self.explode():
                pass
            done = not self.split()
    

    def left_search(self, pred: Callable[[int], bool], update: Callable[[int], Node]) -> bool:
        match self.left, self.right:
            case int(x), _:
                if pred(x):
                    self.left = update(x)
                    return True
                match self.right:
                    case int(x) if pred(x):
                        self.right = update(x)
                        return True
                    case Pair(_):
                        return self.right.left_search(pred, update)
                    
            case Pair(_), _:
                if not self.left.left_search(pred, update):
                    match self.right:
                        case int(x) if pred(x):
                            self.right = update(x)
                            return True
                        case Pair(_):
                            return self.right.left_search(pred, update)
                else:
                    return True
        return False

    def right_search(self, pred: Callable[[int], bool], update: Callable[[int], Node]) -> bool:
        match self.left, self.right:
            case _, int(x):
                if pred(x):
                    self.right = update(x)
                    return True
                match self.left:
                    case int(x) if pred(x):
                        self.left = update(x)
                        return True
                    case Pair(_):
                        return self.left.right_search(pred, update)
            case _, Pair(_):
                if not self.right.right_search(pred, update):
                    match self.left:
                        case int(x) if pred(x):
                            self.left = update(x)
                            return True
                        case Pair(_):
                            return self.left.right_search(pred, update)
                else:
                    return True
        return False

    def split(self) -> bool:
        res =  self.left_search(lambda x: x >= 10, lambda x: Pair(x//2, x//2 + x %2))
        return res
    
    def fragments(self, nesting: int = 0) -> Optional[tuple[bool, tuple[int, int]]]:
        match self.left, self.right:
            case int(x), int(y) if nesting == 4:
                return True, (x, y)
            case Pair(_), int(_):
                
                if frag := self.left.fragments(nesting+1):
                    found, (l, r) = frag
                    if found:
                        self.left = 0
                    self.right += r
                    r = 0
                    return False, (l, r)
            case Pair(_), Pair(_):
                if frag := self.left.fragments(nesting+1):
                    found, (l, r) = frag
                    if found:
                        self.left = 0
                    if r:
                        self.right.left_search(lambda x: True, lambda x: x + r)
                        r = 0
                    return False, (l, r)
                if frag := self.right.fragments(nesting+1):
                    found, (l, r) = frag
                    if found:
                        self.right = 0
                    if l:
                        self.left.right_search(lambda x: True, lambda x: x + l)
                        l = 0

                    return False, (l, r)
            case int(_), Pair(_):
                if frag := self.right.fragments(nesting+1):
                    found, (l, r) = frag            
                    if found:
                        self.right = 0
                    self.left += l
                    l = 0
                    return False, (l, r)

        return None
    

    def explode(self) -> bool:
        if self.fragments(0) is None:
            return False

        return True

    def to_list(self) -> PairList:
        def to_list(nod: Node) -> Union[int, "PairList"]:
            match nod:
                case int(x):
                    return x
                case Pair(_):
                    return nod.to_list()
                case _:
                    raise RuntimeError
        return [to_list(self.left), to_list(self.right)]
    
    def mag(self) -> int:
        def mag(x: Node) -> int:
            if isinstance(x, Pair):
                return x.mag()
            return x
        
        return 3*mag(self.left) + 2*mag(self.right)

def parse_x(x: int | PairList) -> int | Pair:
    match x:
        case [_, _]:
            return Pair.from_list(x)
        case int(_):
            return x
        case _:
            raise RuntimeError(x)

def parse_input(path: str) -> Iterator[Pair]:
    with open(path) as f:
        for line in f:
            yield Pair.from_list(literal_eval(line.rstrip()))


def test_search():
    pair = Pair.from_list([[[[0,7],4],[15,[0,13]]],[1,1]])
    assert pair.left_search(lambda x: x > 10, lambda x: x+2) == True
    assert pair == Pair.from_list([[[[0,7],4],[17,[0,13]]],[1,1]])

    pair = Pair.from_list([[[[0,7],4],[15,[0,13]]],[1,1]])
    assert pair.right_search(lambda x: x > 10, lambda x: x+2) == True
    assert pair == Pair.from_list([[[[0,7],4],[15,[0,15]]],[1,1]])

    pair = Pair.from_list([[[[0,7],4],[5,[0,13]]],[1,1]])
    assert pair.left_search(lambda x: x > 10, lambda x: x+2) == True
    assert pair == Pair.from_list([[[[0,7],4],[5,[0,15]]],[1,1]])
    # assert pair.right_search(lambda x: x > 10) == 13
    # assert pair.left_search(lambda x: x > 15) == None


@pytest.mark.parametrize("before,after", [
    ([[[[[9,8],1],2],3],4], [[[[0,9],2],3],4]),
    ([7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]]),
    ([[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3]),
    ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]),
    ([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]], [[3,[2,[8,0]]],[9,[5,[7,0]]]]),
    ([[[[[3, 0], [5, 3]], [4, 4]], [5, 5]], [6, 6]], [[[[0, [5, 3]], [4, 4]], [5, 5]], [6, 6]])
])
def test_frags(before: PairList, after: PairList):
    a = Pair.from_list(before)
    assert a.to_list() == before
    print(a.fragments())
    assert a == Pair.from_list(after)

@pytest.mark.parametrize("terms,answer", [
    ([
        [1,1],
        [2,2],
        [3,3],
        [4,4],
    ], [[[[1,1],[2,2]],[3,3]],[4,4]]),

    ([
        [1,1],
        [2,2],
        [3,3],
        [4,4],
        [5,5],
    ], [[[[3,0],[5,3]],[4,4]],[5,5]]),

    ([
        [1,1],
        [2,2],
        [3,3],
        [4,4],
        [5,5],
        [6,6],
    ], [[[[5,0],[7,4]],[5,5]],[6,6]]),

    ([
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
        [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
        [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
        [7,[5,[[3,8],[1,4]]]],
        [[2,[2,2]],[8,[8,1]]],
        [2,9],
        [1,[[[9,3],9],[[9,0],[0,7]]]],
        [[[5,[7,4]],7],1],
        [[[[4,2],2],6],[8,7]],
    ], [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])
])
def test_sums(terms: list[PairList], answer: PairList):
    assert reduce(operator.add, (Pair.from_list(l) for l in terms)) == Pair.from_list(answer)

@pytest.mark.parametrize("num,mag", [
    ([[1,2],[[3,4],5]], 143),
    ([[[[0,7],4],[[7,8],[6,0]]],[8,1]], 1384),
    ([[[[1,1],[2,2]],[3,3]],[4,4]], 445),
    ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488),
])
def test_mag(num: PairList, mag: int):
    assert Pair.from_list(num).mag() == mag


def test_full():

    total = reduce(operator.add, parse_input("../inputs/day18_trial.txt"))
    assert total == Pair.from_list([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]])
    assert total.mag() == 4140


def max_pair(pairs: Iterable[Pair]) -> int:
    def mags(pairs: tuple[Pair, Pair]) -> Iterator[int]:
        pair1, pair2 = pairs
        yield (pair1+pair2).mag()
        yield (pair2+pair1).mag()
    mag_pairs = map(mags, itertools.combinations(pairs, 2))
    
    return max( x for p in mag_pairs for x in p)


def test_trial_part2():
    assert max_pair(parse_input("../inputs/day18_trial.txt")) == 3993

if __name__ == "__main__":
    print(reduce(operator.add, parse_input("../inputs/day18.txt")).mag())
    print(max_pair(parse_input("../inputs/day18.txt")))