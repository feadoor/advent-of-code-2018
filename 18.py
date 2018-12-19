from collections import Counter

OPEN = 0
TREE = 1
LUMBER = 2

def parse_char(char):
    return OPEN if char == '.' else (TREE if char == '|' else LUMBER)

def get_diagram():
    with open('data/18.txt', 'r') as f:
        return [[parse_char(c) for c in line.strip()] for line in f]

def neighbours(x, y):
    for nbr in [
        (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1),
        (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]:
        yield nbr


def in_bounds(x, y, diagram):
    return 0 <= x < len(diagram) and 0 <= y < len(diagram[x])

def tick(diagram):
    next_step = [list(x) for x in diagram]
    for x, row in enumerate(diagram):
        for y, val in enumerate(row):
            nbr_counts = Counter(diagram[nx][ny] for nx, ny in neighbours(x, y) if in_bounds(nx, ny, diagram))
            if val == OPEN and nbr_counts[TREE] >= 3:
                next_step[x][y] = TREE
            if val == TREE and nbr_counts[LUMBER] >= 3:
                next_step[x][y] = LUMBER
            if val == LUMBER and (nbr_counts[LUMBER] == 0 or nbr_counts[TREE] == 0):
                next_step[x][y] = OPEN
    return next_step

def counts(diagram):
    return Counter(item for row in diagram for item in row)

def as_string(diagram):
    chars = ['.', '|', '#']
    return ''.join(''.join(chars[v] for v in row) for row in diagram)

def counts_after(n, diagram):
    diagrams, seen, ticks = [diagram], {as_string(diagram): 0}, 0

    while True:
        diagram, ticks = tick(diagram), ticks + 1
        if ticks == n:
            return counts(diagram)
        elif as_string(diagram) not in seen:
            diagrams.append(diagram)
            seen[as_string(diagram)] = ticks
        else:
            period = ticks - seen[as_string(diagram)]
            index = ticks + ((n - ticks) % period) - period
            return counts(diagrams[index])


diagram = get_diagram()
cnts10 = counts_after(10, diagram)
cnts_many = counts_after(1000000000, diagram)
print(cnts10[TREE] * cnts10[LUMBER])
print(cnts_many[TREE] * cnts_many[LUMBER])
