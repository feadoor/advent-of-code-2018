from collections import namedtuple
import re

bot_regex = re.compile('pos=<([^,]+),([^,]+),([^>]+)>, r=(\d+)')

Cube = namedtuple('Cube', ['x', 'y', 'z', 'length'])

class Bot:

    def __init__(self, pos, r):
        self.pos = pos
        self.r = r

    def distance_to(self, other):
        return self.distance_to_point(other.pos)

    def distance_to_point(self, point):
        return sum(abs(c1 - c2) for c1, c2 in zip(self.pos, point))

    def in_range_of(self, cube):
        dx = 0 if cube.x <= self.pos[0] <= cube.x + cube.length else min(abs(cube.x - self.pos[0]), abs(cube.x + cube.length - self.pos[0]))
        dy = 0 if cube.y <= self.pos[1] <= cube.y + cube.length else min(abs(cube.y - self.pos[1]), abs(cube.y + cube.length - self.pos[1]))
        dz = 0 if cube.z <= self.pos[2] <= cube.z + cube.length else min(abs(cube.z - self.pos[2]), abs(cube.z + cube.length - self.pos[2]))
        return (dx + dy + dz) <= self.r

def parse_bot(bot_str):
    match = bot_regex.match(bot_str)
    return Bot(
        (int(match.group(1)), int(match.group(2)), int(match.group(3))),
        int(match.group(4))
    )

def get_bots():
    with open('data/23.txt', 'r') as f:
        return [parse_bot(line) for line in f]

def bots_in_range_of_strongest_bot(bots):
    strongest_bot = max(bots, key=lambda bot: bot.r)
    return sum(1 if strongest_bot.distance_to(bot) <= strongest_bot.r else 0 for bot in bots)

def regions_in_range_of_most_bots(cube, granularity, bots):
    best_hits, best_cubes = 0, []
    for x in range(cube.x, cube.x + cube.length, granularity or 1):
        for y in range(cube.y, cube.y + cube.length, granularity or 1):
            for z in range(cube.z, cube.z + cube.length, granularity or 1):
                test_cube = Cube(x, y, z, granularity)
                hits = sum(1 if bot.in_range_of(test_cube) else 0 for bot in bots)
                if hits > best_hits: best_hits, best_cubes = hits, []
                if hits == best_hits: best_cubes.append(test_cube)
    return best_hits, best_cubes

def bounding_box(bots):
    lx_bot = min(bots, key=lambda bot: bot.pos[0] - bot.r)
    lx = lx_bot.pos[0] - lx_bot.r
    ly_bot = min(bots, key=lambda bot: bot.pos[1] - bot.r)
    ly = ly_bot.pos[1] - ly_bot.r
    lz_bot = min(bots, key=lambda bot: bot.pos[2] - bot.r)
    lz = lz_bot.pos[2] - lz_bot.r

    ux_bot = max(bots, key=lambda bot: bot.pos[0] + bot.r)
    ux = ux_bot.pos[0] + lx_bot.r
    uy_bot = max(bots, key=lambda bot: bot.pos[1] + bot.r)
    uy = uy_bot.pos[1] + ly_bot.r
    uz_bot = max(bots, key=lambda bot: bot.pos[2] + bot.r)
    uz = uz_bot.pos[2] + lz_bot.r

    return lx, ly, lz, ux, uy, uz

def power_of_two_above(n):
    count = 0
    while n > 0:
        n, count = n >> 1, count + 1
    return 1 << count

def point_in_range_of_most_bots(bots):
    bounds = bounding_box(bots)
    granularity = power_of_two_above(max(bounds[3] - bounds[0], bounds[4] - bounds[1], bounds[5] - bounds[2]))
    regions = [Cube(bounds[0], bounds[1], bounds[2], granularity)]

    while granularity > 0:
        granularity, next_regions, best_hits = granularity // 2, [], 0
        for region in regions:
            hits, subregions = regions_in_range_of_most_bots(region, granularity, bots)
            if hits > best_hits: next_regions, best_hits = [], hits
            if hits == best_hits: next_regions += subregions
        regions = next_regions

    points = [(r.x, r.y, r.z) for r in regions]
    return min(points, key=lambda point: sum(abs(c) for c in point))

bots = get_bots()
print(bots_in_range_of_strongest_bot(bots))

closest_point = point_in_range_of_most_bots(bots)
print(sum(abs(c) for c in closest_point))
