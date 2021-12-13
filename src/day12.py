from collections import defaultdict


Neighbours = dict[str, set[str]]


def get_graph(path: str, trim_leaves: bool = True) -> Neighbours:
    neis = defaultdict(set)
    with open(path) as f:
        edges = (tuple(line.rstrip().split("-")) for line in f.readlines())
        for a, b in edges:
            neis[a].add(b)
            neis[b].add(a)

    if trim_leaves:
        leaves = [node for node in neis if [b.islower() for b in neis[node]] == [True]]
        for leaf in leaves:
            del neis[leaf]

    return neis


def paths(neighs: Neighbours):
    lowers = {n for n in neighs if n.islower()}

    def to_end(curr: str, visited: set[str]):
        out = {}

        if "end" in neighs[curr]:
            out["end"] = {}
        next_ns = neighs[curr] - visited - {"end"}
        if next_ns:
            newvis = visited.copy()
            if curr in lowers:
                newvis.add(curr)
            for ns in next_ns:
                out[ns] = to_end(ns, newvis)
        return out

    return to_end("start", set())


def merge(source: dict, destination: dict):
    for key, value in source.items():
        node = destination.setdefault(key, {})
        merge(value, node)
        # if isinstance(value, dict):
        # else:
        #     destination[key] = value

    return destination


def paths_twice(neighs: Neighbours):
    lowers = {n for n in neighs if n.islower()}

    def to_end(curr: str, visited: dict[str, int]):
        out = {}
        for ns in neighs[curr]:
            if ns in visited and (
                (ns == low and visited[ns] > 1) or (ns != low and visited[ns] > 0)
            ):
                continue
            if ns == "end":
                out["end"] = {}
            else:
                newvis = visited.copy()
                if curr in newvis:
                    newvis[curr] += 1
                out[ns] = to_end(ns, newvis)
        return out

    allpaths = {}
    for low in lowers - {"start", "end"}:
        # print()
        # print("low", low)
        newd = to_end("start", {n: 0 for n in lowers})
        # allpaths.append(newd)
        merge(newd, allpaths)
    return allpaths


def listem(d: dict) -> list[list[str]]:
    out = []
    for p, ns in d.items():
        nei_paths = listem(ns)
        if p == "end":
            nei_paths = [["end"]]
        else:
            nei_paths = [[p] + pat for pat in nei_paths]
        out.extend(nei_paths)
    return out


def printem(d: dict):
    for p in listem(d):
        print(",".join(p))


def count_paths(d: dict) -> int:
    ends = (1 if p == "end" else count_paths(ns) for p, ns in d.items())
    return sum(ends)


g = get_graph("../inputs/day12_trial1.txt", trim_leaves=False)
pas = paths_twice(g)
# uniq = set(",".join(p) for p in listem(pas))


# for u in uniq:
#     print(u)

# print(len(uniq))
# for p in listem(pas):
#     print(",".join(p))
# print(pas)
# print(sum(count_paths(p) for p in pas))
print(count_paths(pas))
