from collections import defaultdict, deque

def get_routes():
    with open('data/20.txt', 'r') as f:
        return f.readline().strip()

def move(position, direction):
    x, y = position
    if direction == 'N':
        return x, y + 1
    elif direction == 'S':
        return x, y - 1
    elif direction == 'E':
        return x + 1, y
    elif direction == 'W':
        return x - 1, y

def opposite(direction):
    return {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[direction]

def convert_to_map(routes):
    route_map = defaultdict(set)
    position, position_stack = (0, 0), []
    for char in routes:
        if char in ['N', 'S', 'E', 'W']:
            route_map[position].add(char)
            position = move(position, char)
            route_map[position].add(opposite(char))
        elif char == '(':
            position_stack.append(position)
        elif char == '|':
            position = position_stack[-1]
        elif char == ')':
            position_stack.pop()
    return route_map

def distances(route_map):
    bfs, visited, distances = deque([(0, 0, 0)]), set((0, 0)), defaultdict(int)
    while bfs:
        x, y, distance = bfs.popleft()
        for direction in route_map[(x, y)]:
            nx, ny = move((x, y), direction)
            if not (nx, ny) in visited:
                visited.add((nx, ny))
                bfs.append((nx, ny, distance + 1))
                distances[distance + 1] += 1
    return distances

routes = get_routes()
route_map = convert_to_map(routes)
distances = distances(route_map)

print(max(distances.keys()))
print(sum(v for k, v in distances.items() if k >= 1000))
