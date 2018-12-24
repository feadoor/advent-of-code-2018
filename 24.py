import re

group_re = re.compile("(\d+) units each with (\d+) hit points (?:\((weak|immune) to ([^;\)]*)(?:; (weak|immune) to ([^\)]*))?\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)")

class Group:

    def __init__(self, group_str):
        match = group_re.match(group_str)
        self.units = int(match.group(1))
        self.hp = int(match.group(2))
        self.weaknesses = self.immunities = []

        if match.group(3) == "weak": self.weaknesses = match.group(4).split(', ')
        elif match.group(3) == "immune": self.immunities = match.group(4).split(', ')

        if match.group(5) == "weak": self.weaknesses = match.group(6).split(', ')
        elif match.group(5) == "immune": self.immunities = match.group(6).split(', ')

        self.sp = int(match.group(7))
        self.attack_type = match.group(8)
        self.initiative = int(match.group(9))

def get_armies():
    immune_army = infection_army = []
    with open('data/24a.txt', 'r') as f:
        immune_army = [Group(line) for line in f]
    with open('data/24b.txt', 'r') as f:
        infection_army = [Group(line) for line in f]
    return immune_army, infection_army

def battle(immune_army, infection_army):

    while immune_army and infection_army:

        # Sort by effective power
        immune_army.sort(key=lambda group: (group.units * group.sp, group.initiative), reverse=True)
        infection_army.sort(key=lambda group: (group.units * group.sp, group.initiative), reverse=True)

        # Target selection phase
        selections = {}

        for a_group in immune_army:
            best_damage, selection = 0, None
            for d_group in infection_army:
                damage = 0 if a_group.attack_type in d_group.immunities else a_group.units * a_group.sp
                if a_group.attack_type in d_group.weaknesses: damage *= 2
                if damage > best_damage and d_group not in selections.values(): best_damage, selection = damage, d_group
            selections[a_group] = selection


        for a_group in infection_army:
            best_damage, selection = 0, None
            for d_group in immune_army:
                damage = 0 if a_group.attack_type in d_group.immunities else a_group.units * a_group.sp
                if a_group.attack_type in d_group.weaknesses: damage *= 2
                if damage > best_damage and d_group not in selections.values(): best_damage, selection = damage, d_group
            selections[a_group] = selection

        # Attack phase
        attacking_groups = sorted(immune_army + infection_army, key=lambda group: group.initiative, reverse=True)
        killed_someone = False
        for a_group in attacking_groups:
            if selections[a_group] and a_group.units > 0:
                d_group = selections[a_group]
                damage = 0 if a_group.attack_type in d_group.immunities else a_group.units * a_group.sp
                if a_group.attack_type in d_group.weaknesses: damage *= 2
                killed_units = damage // d_group.hp
                d_group.units -= killed_units
                if killed_units > 0: killed_someone = True

        # Exit early if no-one died
        if not killed_someone: return immune_army, infection_army

        # Cleanup phase
        immune_army = [group for  group in immune_army if group.units > 0]
        infection_army = [group for  group in infection_army if group.units > 0]

    return immune_army, infection_army

def units_in_winning_army():
    immune_army, infection_army = get_armies()
    immune_army, infection_army = battle(immune_army, infection_army)
    if immune_army: return sum(group.units for group in immune_army)
    if infection_army: return sum(group.units for group in infection_army)

def units_left_for_immune_system_after_boost():

    def immune_wins(boost):
        immune_army, infection_army = get_armies()
        for group in immune_army: group.sp += boost
        immune_army, infection_army = battle(immune_army, infection_army)
        return len(immune_army) > 0 and len(infection_army) == 0

    # Can't binary search because it's not true that if a particular boost
    # works then all higher boosts also work. This is because there's the
    # potential to get into a deadlock where immunities mean no damage is dealt
    boost = 0
    while not immune_wins(boost): boost += 1

    immune_army, infection_army = get_armies()
    for group in immune_army: group.sp += boost
    immune_army, infection_army = battle(immune_army, infection_army)
    return sum(group.units for group in immune_army)

print(units_in_winning_army())
print(units_left_for_immune_system_after_boost  ())
