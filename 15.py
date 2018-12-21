from collections import deque
from copy import deepcopy

ATTACK = 3
HP = 200

def get_map():
    with open('data/15.txt', 'r') as f:
        return Map(f.readlines())

class Map:

    def __init__(self, map_str):
        self.map = [[(c != '#') for c in line.strip()] for line in map_str]
        self.units = [[Unit(c) if c in ['E', 'G'] else None for c in line.strip()] for line in map_str]

    def __str__(self):
        def square_str(x, y):
            if not self.map[x][y]:
                return '#'
            elif self.units[x][y]:
                return self.units[x][y].race
            else:
                return '-'

        return '\n'.join(''.join(square_str(x, y) for y in range(len(self.map[x]))) for x in range(len(self.map)))

    def set_elf_attack(self, attack):
        for line in self.units:
            for unit in line:
                if unit and unit.race == 'E':
                    unit.attack = attack

    def count_elves(self):
        return sum(1 if unit.race == 'E' else 0 for line in self.units for unit in line if unit is not None)

    def neighbours(self, square):
        x, y = square
        for nx, ny in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]:
            if self.map[nx][ny] and not self.units[nx][ny]:
                yield nx, ny

    def attacked_squares(self, square):
        x, y = square
        for nx, ny in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]:
            if self.units[nx][ny]:
                yield nx, ny

    def is_target(self, square, unit):
        other = self.units[square[0]][square[1]]
        return other and other.race != unit.race

    def next_step(self, start_square, unit):
        paths, visited = deque([[start_square]]), set(start_square)
        target_paths = []

        while paths:
            path = paths.popleft()
            if any(self.is_target(t, unit) for t in self.attacked_squares(path[-1])):
                target_paths.append(path)
            else:
                for nbr in self.neighbours(path[-1]):
                    if nbr not in visited:
                        visited.add(nbr)
                        paths.append(path + [nbr])

        try:
            return min(target_paths, key=lambda path: (len(path), path[-1]))[1]
        except Exception:
            return start_square

    def perform_round(self):
        move_order = [((x, y), self.units[x][y]) for x in range(len(self.map)) for y in range(len(self.map[x])) if self.units[x][y]]
        for square, unit in move_order:
            if self.units[square[0]][square[1]]:

                nx, ny = self.next_step(square, unit)
                self.units[square[0]][square[1]] = None
                self.units[nx][ny] = unit

                targets = [t for t in self.attacked_squares((nx, ny)) if self.is_target(t, unit)]
                target = min(targets, key=lambda t: (self.units[t[0]][t[1]].hp, t), default=None)
                if target:
                    self.units[target[0]][target[1]].hp -= unit.attack
                    if self.units[target[0]][target[1]].hp <= 0:
                        self.units[target[0]][target[1]] = None

    def total_hp(self):
        units = [unit for line in self.units for unit in line if unit is not None]
        return sum(unit.hp for unit in units)

    def combat_finished(self):
        units = [unit for line in self.units for unit in line if unit is not None]
        races = set(unit.race for unit in units)
        return len(races) <= 1


class Unit:

    def __init__(self, race):
        self.race = race
        self.attack = ATTACK
        self.hp = HP


def part1():
    battlefield, rounds = get_map(), 0
    while not battlefield.combat_finished():
        battlefield.perform_round()
        rounds += 1
    return battlefield.total_hp() * (rounds - 1)

def part2():

    def elves_win_no_losses(attack):
        battlefield = get_map()
        elves = battlefield.count_elves()
        battlefield.set_elf_attack(attack)
        while not battlefield.combat_finished():
            battlefield.perform_round()
        return battlefield.count_elves() == elves

    attack, step = 0, 200
    while (step > 0):
        while not elves_win_no_losses(attack + step):
            attack += step
        step //= 2
    final_attack = attack + 1

    battlefield, rounds = get_map(), 0
    battlefield.set_elf_attack(final_attack)
    while not battlefield.combat_finished():
        battlefield.perform_round()
        rounds += 1
    return battlefield.total_hp() * (rounds - 1)

print(part1())
print(part2())
