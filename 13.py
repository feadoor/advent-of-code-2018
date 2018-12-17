TURN_LEFT = 0
TURN_STRAIGHT = 1
TURN_RIGHT = 2

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3


def replace_cart(track_segment):
    if track_segment == '<' or track_segment == '>':
        return '-'
    elif track_segment == '^' or track_segment == 'v':
        return '|'
    else:
        return track_segment

def is_cart(c):
    return c in ['<', '>', '^', 'v']

def direction_from_cart(cart):
    if cart == '<':
        return LEFT
    elif cart == '>':
        return RIGHT
    elif cart == '^':
        return UP
    elif cart == 'v':
        return DOWN

def next_direction(direction, turn):
    if turn == TURN_STRAIGHT:
        return direction
    elif turn == TURN_LEFT:
        return (direction + 1) % 4
    else:
        return (direction - 1) % 4

def get_track_and_carts():
    with open('data/13.txt', 'r') as f:
        lines = f.readlines()
        track, carts = [[replace_cart(c) for c in line.rstrip()] for line in lines], []
        for i, line in enumerate(lines):
            carts.append([None] * len(line.rstrip()))
            for j, c in enumerate(line.rstrip()):
                if is_cart(c):
                    carts[i][j] = (direction_from_cart(c), TURN_LEFT)
        return track, carts

def tick_return_crash(track, carts):
    ignored_locations = set()
    for i, row in enumerate(carts):
        for j, cart in enumerate(row):
            if cart and not (i, j) in ignored_locations:
                carts[i][j] = None
                direction, turn = cart

                if direction == UP:
                    if carts[i - 1][j]:
                        return i - 1, j
                    elif track[i - 1][j] == '/':
                        carts[i - 1][j] = (RIGHT, turn)
                    elif track[i - 1][j] == '\\':
                        carts[i - 1][j] = (LEFT, turn)
                    elif track[i - 1][j] == '+':
                        carts[i - 1][j] = (next_direction(direction, turn), (turn + 1) % 3)
                    else:
                        carts[i - 1][j] = (direction, turn)

                elif direction == LEFT:
                    if carts[i][j - 1]:
                        return i, j - 1
                    elif track[i][j - 1] == '/':
                        carts[i][j - 1] = (DOWN, turn)
                    elif track[i][j - 1] == '\\':
                        carts[i][j - 1] = (UP, turn)
                    elif track[i][j - 1] == '+':
                        carts[i][j - 1] = (next_direction(direction, turn), (turn + 1) % 3)
                    else:
                        carts[i][j - 1] = (direction, turn)

                if direction == DOWN:
                    if carts[i + 1][j]:
                        return i + 1, j
                    elif track[i + 1][j] == '/':
                        carts[i + 1][j] = (LEFT, turn)
                    elif track[i + 1][j] == '\\':
                        carts[i + 1][j] = (RIGHT, turn)
                    elif track[i + 1][j] == '+':
                        carts[i + 1][j] = (next_direction(direction, turn), (turn + 1) % 3)
                    else:
                        carts[i + 1][j] = (direction, turn)
                    ignored_locations.add((i + 1, j))

                if direction == RIGHT:
                    if carts[i][j + 1]:
                        return i, j + 1
                    elif track[i][j + 1] == '/':
                        carts[i][j + 1] = (UP, turn)
                    elif track[i][j + 1] == '\\':
                        carts[i][j + 1] = (DOWN, turn)
                    elif track[i][j + 1] == '+':
                        carts[i][j + 1] = (next_direction(direction, turn), (turn + 1) % 3)
                    else:
                        carts[i][j + 1] = (direction, turn)
                    ignored_locations.add((i, j + 1))

def tick_remove_crashes_return_count(track, carts):
    ignored_locations = set()
    count = 0
    for i, row in enumerate(carts):
        for j, cart in enumerate(row):
            if cart and not (i, j) in ignored_locations:
                count += 1
                carts[i][j] = None
                direction, turn = cart

                if direction == UP:
                    if carts[i - 1][j]:
                        carts[i - 1][j] = None
                        count -= 2
                    elif track[i - 1][j] == '/':
                        carts[i - 1][j] = (RIGHT, turn)
                    elif track[i - 1][j] == '\\':
                        carts[i - 1][j] = (LEFT, turn)
                    elif track[i - 1][j] == '+':
                        carts[i - 1][j] = (next_direction(direction, turn), (turn + 1) % 3)
                    else:
                        carts[i - 1][j] = (direction, turn)

                elif direction == LEFT:
                    if carts[i][j - 1]:
                        carts[i][j - 1] = None
                        count -= 2
                    elif track[i][j - 1] == '/':
                        carts[i][j - 1] = (DOWN, turn)
                    elif track[i][j - 1] == '\\':
                        carts[i][j - 1] = (UP, turn)
                    elif track[i][j - 1] == '+':
                        carts[i][j - 1] = (next_direction(direction, turn), (turn + 1) % 3)
                    else:
                        carts[i][j - 1] = (direction, turn)

                if direction == DOWN:
                    if carts[i + 1][j]:
                        carts[i + 1][j] = None
                        count -= 2
                    elif track[i + 1][j] == '/':
                        carts[i + 1][j] = (LEFT, turn)
                    elif track[i + 1][j] == '\\':
                        carts[i + 1][j] = (RIGHT, turn)
                    elif track[i + 1][j] == '+':
                        carts[i + 1][j] = (next_direction(direction, turn), (turn + 1) % 3)
                    else:
                        carts[i + 1][j] = (direction, turn)
                    ignored_locations.add((i + 1, j))

                if direction == RIGHT:
                    if carts[i][j + 1]:
                        carts[i][j + 1] = None
                        count -= 2
                    elif track[i][j + 1] == '/':
                        carts[i][j + 1] = (UP, turn)
                    elif track[i][j + 1] == '\\':
                        carts[i][j + 1] = (DOWN, turn)
                    elif track[i][j + 1] == '+':
                        carts[i][j + 1] = (next_direction(direction, turn), (turn + 1) % 3)
                    else:
                        carts[i][j + 1] = (direction, turn)
                    ignored_locations.add((i, j + 1))

    return count

def first_collision():
    track, carts = get_track_and_carts()
    collision = None
    while collision is None:
        collision = tick_return_crash(track, carts)
    return (collision[1], collision[0])

def last_cart():
    track, carts = get_track_and_carts()
    count = sum(sum(1 if cart else 0 for cart in row) for row in carts)
    while count > 1:
        count = tick_remove_crashes_return_count(track, carts)
    for i, row in enumerate(carts):
        for j, cart in enumerate(row):
            if cart:
                return j, i

print(first_collision())
print(last_cart())
