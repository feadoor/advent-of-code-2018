from itertools import count

INITIAL_STATE = '..#..###...#####.#.#...####.#..####..###.##.#.#.##.#....#....#.####...#....###.###..##.#....#######'

class State:

    def __init__(self, s, update_map):
        self.state = [char == '#' for char in INITIAL_STATE]
        self.start_idx = 0
        self.update_map = update_map

    def tick(self):
        self.buffer()

        bitmask, new_state = 0, []
        for idx in range(len(self.state) - 2):
            bitmask = (bitmask >> 1) + (16 if self.state[idx + 2] else 0)
            new_state.append(self.update_map[bitmask])
        self.state = new_state

        self.trim()

    def _starting_empties(self):
        for i, x in enumerate(self.state):
            if x: return i

    def _ending_empties(self):
        for i, x in enumerate(reversed(self.state)):
            if x: return i

    def buffer(self):
        start, end = 5 - self._starting_empties(), 5 - self._ending_empties()
        self.state = [False] * start + self.state + [False] * end
        self.start_idx -= start

    def trim(self):
        start, end = max(0, self._starting_empties() - 5), max(0, self._ending_empties() - 5)
        self.state = self.state[start : len(self.state) -  end]
        self.start_idx += start

    def sum_of_alive_pots(self):
        return sum(x if b else 0 for x, b in zip(count(self.start_idx), self.state))


def get_update_map():
    with open('data/12.txt', 'r') as f:
        updates = [False] * 32
        for line in f:
            bitmask = sum(1 << i if line[i] == '#' else 0 for i in range(5))
            result = (line[9] == '#')
            updates[bitmask] = result
        return updates

def sum_after_20(update_map):
    state = State(INITIAL_STATE, update_map)
    for tick in range(20):
        state.tick()
    return state.sum_of_alive_pots()

def sum_after_n(update_map, n):
    state = State(INITIAL_STATE, update_map)
    ticks, total, differences = 0, state.sum_of_alive_pots(), []

    while ticks < n and (len(differences) < 100 or not all(x == differences[-1] for x in differences[-100:])):
        state.tick()
        ticks, new_total = ticks + 1, state.sum_of_alive_pots()
        differences.append(new_total - total)
        total = new_total

    difference, ticks_remaining = differences[-1], n - ticks
    return total + ticks_remaining * difference

update_map = get_update_map()
print(sum_after_20(update_map))
print(sum_after_n(update_map, 50000000000))
