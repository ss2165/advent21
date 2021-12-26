import itertools
from typing import Generic, Iterator, Optional, TypeVar, cast
from dataclasses import dataclass, field
import networkx as nx
import sys
import heapq

from networkx.classes.graph import Graph


# D#C#B#A#
# D#B#A#C#
# INSTR = "BACDBCDA"
# INSTR = "BDBCCADA"
# INSTR = "BDDACCBDBBACDACA"
INSTR = "BDDDBCBCCBAADACA"
HALLWAY_SIZE = 11
N_ROOMS = 4
ROOM_SIZE = len(INSTR) // N_ROOMS
ROOM_ENTRANCES = frozenset(range(2, HALLWAY_SIZE - 2, 2))


def room_first(room: int) -> int:
    return HALLWAY_SIZE + room * ROOM_SIZE


def room_entrance(room: int) -> int:
    return 2 * (room + 1)


def room_index(pos: int) -> int:
    return (pos - HALLWAY_SIZE) // ROOM_SIZE


def in_hallway(pos: int) -> bool:
    return pos < HALLWAY_SIZE


def in_room(pos: int, room: int) -> bool:
    r0 = room_first(room)
    return (pos - r0) in range(ROOM_SIZE)


def pos_in_room(pos: int) -> int:
    return (pos - HALLWAY_SIZE) % ROOM_SIZE


def back_of_room(pos: int) -> bool:
    return pos_in_room(pos) == (ROOM_SIZE - 1)


def gen_dists() -> dict[int, dict[int, int]]:
    G = nx.Graph()
    G.add_edges_from((i, i + 1) for i in range(HALLWAY_SIZE - 1))

    for room in range(N_ROOMS):
        r0 = room_first(room)
        G.add_edges_from((i + r0, i + r0 + 1) for i in range(ROOM_SIZE - 1))
        G.add_edge(room_entrance(room), r0)
    return dict(nx.all_pairs_shortest_path_length(G))


DISTS = gen_dists()


@dataclass(frozen=True)
class State:
    state: tuple[frozenset[int], frozenset[int], frozenset[int], frozenset[int]]

    @classmethod
    def from_str(cls, code: str) -> "State":
        return State(
            tuple(
                frozenset(i + HALLWAY_SIZE for i, c2 in enumerate(code) if c2 == c)
                for c in "ABCD"
            )
        )

    def is_occupied(self, pos: int) -> bool:
        return any(i == pos for c in self.state for i in c)

    def way_clear(self, move: tuple[int, int]) -> bool:
        start, end = move
        if not in_hallway(start):
            r_i = room_index(start)
            if any(self.is_occupied(j) for j in range(room_first(r_i), start)):
                return False
            start = room_entrance(r_i)
        if not in_hallway(end):
            r_i = room_index(end)
            if any(self.is_occupied(j) for j in range(room_first(r_i), end)):
                return False
            end = room_entrance(r_i)

        search_range = (
            range(start + 1, end) if end > start else range(start - 1, end, -1)
        )
        for j in search_range:
            if self.is_occupied(j):
                return False

        return True

    def possible_moves(self) -> Iterator[tuple[int, int]]:
        for target, curr_poses in enumerate(self.state):
            for cur_pos in curr_poses:
                if in_room(cur_pos, target) and back_of_room(cur_pos):
                    continue
                if not in_hallway(cur_pos) and not self.way_clear(
                    (cur_pos, room_first(room_index(cur_pos)))
                ):
                    continue
                rf = room_first(target)
                for r_pos in range(rf + ROOM_SIZE - 1, rf - 1, -1):
                    if not self.is_occupied(r_pos):
                        move = (cur_pos, r_pos)
                        if self.way_clear(move):
                            yield move
                    if r_pos not in self.state[target]:
                        break

                if in_hallway(cur_pos):
                    continue

                for j in range(room_entrance(room_index(cur_pos)) - 1, -1, -1):
                    if self.is_occupied(j):
                        break
                    if j not in ROOM_ENTRANCES:
                        yield (cur_pos, j)

                for j in range(room_entrance(room_index(cur_pos)) + 1, HALLWAY_SIZE):
                    if self.is_occupied(j):
                        break
                    if j not in ROOM_ENTRANCES:
                        yield (cur_pos, j)

    def score_move(self, start: int, end: int) -> int:
        target = next(i for i, c in enumerate(self.state) if start in c)
        return DISTS[start][end] * 10 ** (target)

    def make_move(self, start: int, end: int) -> "State":
        return State(
            tuple(
                frozenset((end if pos == start else pos) for pos in target)
                for target in self.state
            )
        )

    def neighbours(self) -> Iterator[tuple["State", int]]:
        for move in self.possible_moves():
            yield self.make_move(*move), self.score_move(*move)

    def heuristic_distance(self, other: "State") -> int:
        return sum(
            min(
                sum(self.score_move(x, y) for x, y in zip(a_perm, hes))
                for a_perm in itertools.permutations(mes, len(hes))
            )
            for mes, hes in zip(self.state, other.state)
        )


COMPLETED_STATE = State(
    tuple(
        (
            frozenset(range(room_first(room), room_first(room) + ROOM_SIZE))
            for room in range(N_ROOMS)
        )
    )
)

min_cache: dict[State, Optional[tuple[int, list[tuple[int, int]]]]] = {}

cache_hit = 0


def min_score(
    st: State,
    accum: int,
    return_moves: bool = False,
) -> Optional[tuple[int, list[tuple[int, int]]]]:
    if st == COMPLETED_STATE:
        return accum, list()

    mins: list[tuple[int, list[tuple[int, int]]]] = []

    num_trials = 0
    max_trials = 3
    for move in st.possible_moves():
        if num_trials > max_trials:
            break
        cost = st.score_move(*move)
        newst = st.make_move(*move)
        if newst in min_cache:
            new_mins = min_cache[newst]
            if new_mins is None:
                continue
            else:
                num_trials += 1
            global cache_hit
            cache_hit += 1
            new_min, moves = new_mins
            upmoves = [move] + moves if return_moves else []
            mins.append((new_min + cost + accum, upmoves))

        else:
            min_cache[newst] = None
            new_mins = min_score(newst, cost + accum, return_moves=return_moves)
            if new_mins is not None:
                new_min, moves = new_mins

                min_cache[newst] = (new_min - cost - accum, moves)
                upmoves = [move] + moves if return_moves else []
                mins.append((new_min, upmoves))
            else:
                num_trials += 1

    minf = min(mins, key=lambda x: x[0]) if mins else None
    if minf is None:
        return None
    return minf[0], minf[1]


Item = TypeVar("Item")


@dataclass(order=True)
class PriorityItem(Generic[Item]):
    priority: int
    entry: int
    item: Optional[Item] = field(compare=False)

    def is_removed(self) -> bool:
        return self.item is None

    def remove(self):
        self.item = None


class PriorityQueue(Generic[Item]):
    def __init__(self) -> None:
        self.h: list[PriorityItem[Item]] = []
        self.entry_finder: dict[Item, PriorityItem[Item]] = {}
        self.counter = itertools.count()

    def insert(self, item: Item, priority: int = 0):
        if item in self.entry_finder:
            self.remove(item)

        count = next(self.counter)
        entry = PriorityItem(priority, count, item)

        self.entry_finder[item] = entry
        heapq.heappush(self.h, entry)

    def remove(self, item: Item):
        entry = self.entry_finder.pop(item)
        entry.remove()

    def pop(self) -> Item:
        while self.h:
            entry = heapq.heappop(self.h)
            if not entry.is_removed():
                item = cast(Item, entry.item)
                del self.entry_finder[item]
                return item
        raise KeyError


def astar(st: State, target: State) -> int:
    h = lambda x: target.heuristic_distance(x)
    fringe: PriorityQueue[State] = PriorityQueue()
    fringe.insert(st, 0)
    scores = {}
    scores[st] = 0

    fscores = {}
    fscores[st] = h(st)

    while fringe.h:
        curst = fringe.pop()
        if curst == target:
            return scores[COMPLETED_STATE]

        for neigh, score in curst.neighbours():
            newscore = scores[curst] + score
            if neigh not in scores or newscore < scores[neigh]:
                scores[neigh] = newscore
                fscores[neigh] = newscore + h(neigh)
                if neigh not in fringe.entry_finder:
                    fringe.insert(neigh, fscores[neigh])
    return -1


def build_state_graph(st: State) -> nx.Graph:
    G = Graph()

    to_add = {st}
    added = set()
    while to_add:
        curst = to_add.pop()
        added.add(curst)
        if curst == COMPLETED_STATE:
            continue
        for neigh, score in curst.neighbours():
            if neigh not in added:
                to_add.add(neigh)
            G.add_edge(curst, neigh, weight=score)
    del to_add
    del added
    return G

start = State.from_str(INSTR)
print(astar(start, COMPLETED_STATE))
