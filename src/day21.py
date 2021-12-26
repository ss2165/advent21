from typing import Iterator
import itertools
from collections import Counter


def determ_dice() -> Iterator[int]:
    return itertools.cycle(range(1, 101))


def part1():
    positions = [4, 8]
    scores = [0, 0]

    dice = determ_dice()
    dicerolls = 0

    while max(scores) < 1000:
        for i in range(len(positions)):
            dicerolls += 3
            roll = sum(itertools.islice(dice, 3))
            positions[i] = (positions[i] + roll - 1) % 10 + 1
            scores[i] += positions[i]

            if scores[i] >= 1000:
                break

    print(min(scores))
    print(dicerolls)

    print(min(scores) * dicerolls)


def part2():
    one_dirac_rolls = Counter(map(sum, itertools.product(*([[1, 2, 3]] * 3))))
    dirac_rolls = Counter(itertools.product(one_dirac_rolls.elements(), one_dirac_rolls.elements()))
    state_dist: Counter[tuple[tuple[int, int], tuple[int, int]]] = Counter({((4, 0), (8,0)): 1})
    n1_wins = 0
    n2_wins = 0

    rounds = 0
    while state_dist:
        rounds += 1

        new_p1_pos_dist = Counter()
        for ((p1, s1), (p2, s2)), pos_count in state_dist.items():
            for (roll1, roll2), roll_count in dirac_rolls.items():

                newp1 = (p1 + roll1 - 1) % 10 + 1
                new_s1 = s1 + newp1
                newp2 = (p2 + roll2 - 1) % 10 + 1
                new_s2 = s2 + newp2
                n_inst = pos_count * roll_count

                    
                if new_s1 >= 21:
                    n1_wins += n_inst
                elif new_s2 >= 21:
                    n2_wins += n_inst
                else:
                    new_p1_pos_dist[((newp1, new_s1), (newp2, new_s2))] += n_inst

        state_dist = new_p1_pos_dist
        print(len(state_dist))
        # completed = [pair for pair in p1_pos_dist if pair[0][1] >= 21 or pair[1][1] >= 21]
        # for comp in completed:
        #     if comp[0][1] >= 21:
        #         n1_wins += p1_pos_dist[comp]
        #     else:
        #         n2_wins += p1_pos_dist[comp]
        #     del p1_pos_dist[comp]

        
        # new_p1_pos_dist = Counter()
        # for (pos, score), pos_count in p2_pos_dist.items():
        #     for roll, roll_count in dirac_rolls.items():

        #         newp1 = (pos + roll - 1) % 10 + 1
        #         new_score = score + newp1
        #         new_p1_pos_dist[(newp1, new_score)] = pos_count * roll_count

        # p2_pos_dist = new_p1_pos_dist

        # completed = [pair for pair in p2_pos_dist if pair[1]>=21]
        # for comp in completed:
        #     n2_wins += p2_pos_dist[comp]
        #     del p2_pos_dist[comp]
    print(n1_wins, n2_wins)
    print(rounds)

part2()