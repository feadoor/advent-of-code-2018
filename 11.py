from itertools import product

GRID_SIZE = 300
SERIAL = 9005

def get_power_levels():
    power_levels = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for x in range(1, GRID_SIZE + 1):
        for y in range(1, GRID_SIZE + 1):
            base_power = ((x + 10) * y + SERIAL) * (x + 10)
            hundreds = (base_power % 1000) // 100
            power_levels[x - 1][y - 1] = hundreds - 5
    return power_levels

def largest_3square(power_levels):
    best, best_x, best_y = -float("inf"), None, None
    for x in range(GRID_SIZE - 2):
        for y in range(GRID_SIZE - 2):
            total = sum(power_levels[xx][yy] for xx, yy in product(range(x, x + 3), range(y, y + 3)))
            if total > best:
                best, best_x, best_y = total, x, y
    return (best_x + 1, best_y + 1)

def best_contiguous_sum(arr, length):
    acc = sum(arr[:length])
    best, best_idx = acc, 0
    for i in range(length, len(arr) - length + 1):
        acc = acc - arr[i - length] + arr[i]
        if acc > best:
            best, best_idx = acc, i - length + 1
    return best, best_idx

def largest_square(power_levels):
    row_sums = [[0] for _ in range(GRID_SIZE)]
    for i, row in enumerate(power_levels):
        for v in row:
            row_sums[i].append(row_sums[i][-1] + v)

    best, best_x, best_y, best_size = -float("inf"), None, None, None
    for size in range(1, GRID_SIZE + 1):
        for y in range(GRID_SIZE - size):
            squashed_sums = [row_sums[x][y + size] - row_sums[x][y] for x in range(GRID_SIZE)]
            total, x = best_contiguous_sum(squashed_sums, size)
            if total > best:
                best, best_x, best_y, best_size = total, x, y, size

    return (best_x + 1, best_y + 1, best_size)


power_levels = get_power_levels()
print(largest_3square(power_levels))
print(largest_square(power_levels))
