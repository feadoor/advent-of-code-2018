from itertools import product
import re
from sys import setrecursionlimit
from time import sleep

setrecursionlimit(10000)

SAND = 0
CLAY = 1
REACHED = 2
SETTLED = 3

range_re = re.compile('(?:(\d+$)|(\d+..\d+$))')
line_re = re.compile('(\w)=([^,]*), (\w)=(.*)')

def parse_range(range_str):
    match = range_re.match(range_str)
    if match.group(2):
        start, end = [int(x)for x in match.group(2).split('..')]
        return start, end
    else:
        start = int(match.group(1))
        return start, start

def parse_line(line):
    ranges = line_re.match(line)
    if ranges.group(1) == 'x':
        x_range, y_range = parse_range(ranges.group(2)), parse_range(ranges.group(4))
    else:
        x_range, y_range = parse_range(ranges.group(4)), parse_range(ranges.group(2))
    return x_range, y_range

def get_diagram():
    with open('data/17.txt', 'r') as f:
        ranges = [parse_line(line) for line in f]
        x_bounds = min(r[0][0] for r in ranges), max(r[0][1] for r in ranges)
        y_bounds = min(r[1][0] for r in ranges), max(r[1][1] for r in ranges)
        diagram = [[SAND] * (y_bounds[1] + 2) for _ in range(x_bounds[1] + 2)]
        for (x1, x2), (y1, y2) in ranges:

            for x, y in product(range(x1, x2 + 1), range(y1, y2 + 1)):
                diagram[x][y] = CLAY
        return ((x_bounds, y_bounds), diagram)

def fill_diagram(diagram, source):

    width, height = len(diagram), len(diagram[0])

    def free(x, y):
        return not (0 <= x < width and 0 <= y < height) or diagram[x][y] in [SAND, REACHED]

    def inner_fill(src):
        # print(repr(diagram, ((max(0, src[0] - 25), min(width - 1, src[0] + 25)), (max(0, src[1] - 25), min(height - 1, src[1] + 25)))), '\n\n')
        # sleep(0.02)

        if src[0] < 0 or src[0] >= width or src[1] < 0 or src[1] >= height or not free(*src):
            return

        if not free(src[0], src[1] + 1):
            left, right = src[0], src[0] + 1
            while free(left, src[1]) and not free(left, src[1] + 1):
                diagram[left][src[1]] = REACHED
                left -= 1
            while free(right, src[1]) and not free(right, src[1] + 1):
                diagram[right][src[1]] = REACHED
                right += 1

            if left >= 0 and right < width and diagram[left][src[1]] == CLAY and diagram[right][src[1]] == CLAY:
                for x in range(left + 1, right):
                    diagram[x][src[1]] = SETTLED
            else:
                if free(left, src[1] + 1) or free(right, src[1] + 1):
                    inner_fill((left, src[1]))
                if free(right, src[1] + 1):
                    inner_fill((right, src[1]))

        elif diagram[src[0]][src[1]] == SAND:
            diagram[src[0]][src[1]] = REACHED
            inner_fill((src[0], src[1] + 1))
            if src[1] < height - 1 and diagram[src[0]][src[1] + 1] == SETTLED:
                inner_fill(src)

    inner_fill(source)

def count_reached(diagram, bounds):
    (x1, x2), (y1, y2) = bounds
    return sum(1 if diagram[x][y] in [SETTLED, REACHED] else 0 for x, y in product(range(x1 - 1, x2 + 2), range(y1, y2 + 1)))

def count_settled(diagram, bounds):
    (x1, x2), (y1, y2) = bounds
    return sum(1 if diagram[x][y] == SETTLED else 0 for x, y in product(range(x1 - 1, x2 + 2), range(y1, y2 + 1)))

def repr(diagram, bounds):
    chars = ['.', '#', '|', '~']
    (x1, x2), (y1, y2) = bounds
    return '\n'.join(''.join(chars[diagram[x][y]] for x in range(x1 - 1, x2 + 2)) for y in range(y1, y2 + 1))

bounds, diagram = get_diagram()
fill_diagram(diagram, (500, 0))
# print(repr(diagram, bounds))
print(count_reached(diagram, bounds))
print(count_settled(diagram, bounds))
