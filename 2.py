from collections import Counter
from itertools import combinations

def get_strings():
    with open('data/2.txt', 'r') as f:
        return [line.strip() for line in f]

def get_checksum(strings):
    counts = [Counter(s) for s in strings]
    twos = sum(1 for x in counts if 2 in x.values())
    threes = sum(1 for x in counts if 3 in x.values())
    return twos * threes

def distance(s, t):
    return sum(1 for x in zip(s, t) if x[0] != x[1])

def get_common_letters(strings):
    for s, t in combinations(strings, 2):
        if distance(s, t) == 1:
            return ''.join(x[0] for x in zip(s, t) if x[0] == x[1])

strings = get_strings()
print(get_checksum(strings))
print(get_common_letters(strings))