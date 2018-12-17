from collections import namedtuple, defaultdict
from itertools import combinations, product
import re

claim_regex = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

class Claim:

    def __init__(self, iden, left, top, width, height):
        self.id = int(iden)
        self.left = int(left)
        self.top = int(top)
        self.width = int(width)
        self.height = int(height)

    @property
    def right(self):
        return self.left + self.width - 1

    @property
    def bottom(self):
        return self.top + self.height - 1

    def squares(self):
        return product(range(self.left, self.right + 1), range(self.top, self.bottom + 1))

    def _overlaps(self, other):
        return (self.bottom >= other.top  and other.bottom >= self.top and
                self.right  >= other.left and other.right  >= self.left)

    def __and__(self, other):
        return self._overlaps(other)


def get_claims():
    with open('data/3.txt', 'r') as f:
        return [parse_claim(line) for line in f]

def parse_claim(s):
    match = claim_regex.match(s)
    return Claim(*(match.group(i) for i in range(1, 6)))

def get_overlaps(claims):
    covered = defaultdict(int)
    for claim in claims:
        for x, y in claim.squares():
            covered[(x, y)] += 1
    return sum(1 for v in covered.values() if v > 1)

def is_lonely(claim):
    for other in claims:
        if (other.id != claim.id) and claim & other:
            return False
    return True

def get_lonely_claim(claims):
    for claim in claims:
        if is_lonely(claim):
            return claim.id

claims = get_claims()
print(get_overlaps(claims))
print(get_lonely_claim(claims))

