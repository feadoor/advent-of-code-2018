class DisjointSetDataStructure:

    def __init__(self, obj):
        self.obj    = obj
        self.rank   = 0
        self.parent = self

    def find_set(self):
        if self.parent != self:
            self.parent = self.parent.find_set()
        return self.parent

    def union(self, other):
        self_root = self.find_set()
        other_root = other.find_set()

        if self_root == other_root:
            return

        if self_root.rank < other_root.rank:
            self_root.parent = other_root
        elif self_root.rank > other_root.rank:
            other_root.parent = self_root
        else:
            other_root.parent = self_root
            self_root.rank += 1

def get_points():
    with open('data/25.txt', 'r') as f:
        return [tuple(int(x) for x in line.strip().split(',')) for line in f]

def distance(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))

def number_of_constellations(points):
    constellations = [DisjointSetDataStructure(point) for point in points]
    for idx, constellation in enumerate(constellations):
        for jdx in range(idx):
            if distance(constellation.obj, constellations[jdx].obj) <= 3:
                constellation.union(constellations[jdx])
    return len(set(constellation.find_set() for constellation in constellations))

points = get_points()
print(number_of_constellations(points))
