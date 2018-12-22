import heapq

DEPTH = 4002
TARGET = 5, 746

def get_erosion_levels(width, height, target):
    MODULUS, erosions = 20183, [[0] * (height + 1) for _ in range(width + 1)]
    erosions[0][0] = DEPTH % MODULUS
    for y in range(height + 1):
        erosions[0][y] = (48271 * y + DEPTH) % MODULUS
    for x in range(width + 1):
        erosions[x][0] = (16807 * x + DEPTH) % MODULUS
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            if x == target[0] and y == target[1]:
                erosions[x][y] = DEPTH % MODULUS
            else:
                erosions[x][y] = (erosions[x - 1][y] * erosions[x][y - 1] + DEPTH) % MODULUS
    return erosions

def get_risk(target):
    erosion_levels = get_erosion_levels(target[0], target[1], target)
    return sum(sum(l % 3 for l in row) for row in erosion_levels)

def shortest_path_to_target(target):
    erosion_levels = get_erosion_levels(max(1000, 2 * target[0]), max(1000, 2 * target[1]), target)
    region_types = [[l % 3 for l in row] for row in erosion_levels]

    def neighbours(x, y, tool):
        region_type = region_types[x][y]
        for new_tool in range(3):
            if new_tool != region_type and new_tool != tool:
                yield (7, (x, y, new_tool))
        for new_x, new_y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= new_x < len(region_types) and 0 <= new_y < len(region_types[new_x]) and tool != region_types[new_x][new_y]:
                yield (1, (new_x, new_y, tool))

    distances = [[[float('inf')] * 3 for _ in row] for row in region_types]
    visited = [[[False] * 3 for _ in row] for row in region_types]
    distances[0][0][1] = 0
    pq = [(0, (0, 0, 1))]

    while pq:
        _, (x, y, tool) = heapq.heappop(pq)
        if (x, y, tool) == (target[0], target[1], 1):
            return distances[x][y][tool]
        elif not visited[x][y][tool]:
            for distance, (new_x, new_y, new_tool) in neighbours(x, y, tool):
                if distances[new_x][new_y][new_tool] > distance + distances[x][y][tool]:
                    distances[new_x][new_y][new_tool] = distance + distances[x][y][tool]
                    heapq.heappush(pq, (distances[new_x][new_y][new_tool], (new_x, new_y, new_tool)))
            visited[x][y][tool] = True

print(get_risk(TARGET))
print(shortest_path_to_target(TARGET))
