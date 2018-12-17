from operator import itemgetter
import re

point_regex = re.compile('position=<([^,]+), ([^>]+)> velocity=<([^,]+), ([^>]+)>')

class Point:

    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity

    def moved(self, ticks):
        position = (
            self.pos[0] + self.velocity[0] * ticks,
            self.pos[1] + self.velocity[1] * ticks
        )
        return Point(position, self.velocity)

def parse_point(point_str):
    match = point_regex.match(point_str)
    return Point(
        (int(match.group(1)), int(match.group(2))),
        (int(match.group(3)), int(match.group(4)))
    )

def get_points():
    with open('data/10a.txt', 'r') as f:
        return [parse_point(line) for line in f]

def moved(points, ticks):
    return [point.moved(ticks) for point in points]

def bounding_box(points):
    positions = [point.pos for point in points]
    min_x, max_x = min(positions, key=itemgetter(0))[0], max(positions, key=itemgetter(0))[0]
    min_y, max_y = min(positions, key=itemgetter(1))[1], max(positions, key=itemgetter(1))[1]
    return ((min_x, max_x), (min_y, max_y))

def box_size(points):
    (min_x, max_x), (min_y, max_y) = bounding_box(points)
    return (max_x - min_x) * (max_y - min_y)

def message(points):
    (min_x, max_x), (min_y, max_y) = bounding_box(points)
    message = [['.'] * (max_x - min_x + 1) for _ in range(min_y, max_y + 1)]
    for point in points:
        message[point.pos[1] - min_y][point.pos[0] - min_x] = '#'
    return '\n'.join(''.join(row) for row in message)

def ticks_for_message(points):

    def size_after_ticks(ticks):
        return box_size(moved(points, ticks))

    points, ticks, jump_size = get_points(), -1, 1
    while size_after_ticks(jump_size) < box_size(points):
        jump_size *= 2
    while jump_size > 0:
        if size_after_ticks(ticks + jump_size) > size_after_ticks(ticks + jump_size + 1):
            ticks += jump_size
        jump_size //= 2

    return ticks + 1

points = get_points()
ticks = ticks_for_message(points)
print(message(moved(points, ticks)))
print(ticks)
