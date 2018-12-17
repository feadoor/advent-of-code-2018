from collections import defaultdict
from itertools import product
from operator import itemgetter

def get_points():
    with open('data/6.txt', 'r') as f:
        return [tuple(int(x) for x in line.split(',')) for line in f]

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_closest_point_idx(p, points):
    min_val, min_idx = float("inf"), None
    distances = [distance(p, pt) for pt in points]
    for i, d in enumerate(distances):
        if d < min_val:
            min_val, min_idx = d, i
        elif d == min_val:
            min_idx = None
    return min_idx

def get_largest_finite_area(points):
    areas, closest_points = defaultdict(int), dict()
    min_x, max_x = min(points, key=itemgetter(0))[0] - 1, max(points, key=itemgetter(0))[0] + 1
    min_y, max_y = min(points, key=itemgetter(1))[1] - 1, max(points, key=itemgetter(1))[1] + 1

    for x, y in product(range(min_x, max_x + 1), range(min_y, max_y + 1)):
        closest_point = get_closest_point_idx((x, y), points)
        if closest_point is not None:
            areas[closest_point] += 1
            closest_points[(x, y)] = closest_point

    for x in range(min_x, max_x + 1):
        areas.pop(closest_points.get((x, min_y), None), None)
        areas.pop(closest_points.get((x, max_y), None), None)
    for y in range(min_y, max_y + 1):
        areas.pop(closest_points.get((min_x, y), None), None)
        areas.pop(closest_points.get((max_x, y), None), None)

    return max(areas.values())

def get_safe_region_size(points):
    threshold = 10000
    min_x, max_x = min(points, key=itemgetter(0))[0] - 1, max(points, key=itemgetter(0))[0] + 1
    min_y, max_y = min(points, key=itemgetter(1))[1] - 1, max(points, key=itemgetter(1))[1] + 1
    buffer_zone = threshold // len(points) // 2

    count = 0
    for x in range(min_x - buffer_zone, max_x + buffer_zone + 1):
        for y in range(min_y - buffer_zone, max_y + buffer_zone + 1):
            if sum(distance((x, y), pt) for pt in points) < threshold:
                count += 1

    return count

points = get_points()
print(get_largest_finite_area(points))
print(get_safe_region_size(points))