from copy import deepcopy
from collections import defaultdict
import re

dependency_regex = re.compile('Step (\w+) must be finished before step (\w+) can begin')

def parse_dependency(line):
    match = dependency_regex.match(line)
    return (match.group(1), match.group(2))

def get_dependencies():
    dependencies = defaultdict(set)
    with open('data/7.txt', 'r') as f:
        for line in f:
            before, after = parse_dependency(line)
            dependencies[before] = dependencies.get(before, set())
            dependencies[after].add(before)
        return dependencies

def get_order(dependencies):
    dependencies, order = deepcopy(dependencies), []
    while dependencies:
        next_steps = [k for k, v in dependencies.items() if not v]
        next_step = min(next_steps)
        del dependencies[next_step]
        for v in dependencies.values():
            if next_step in v:
                v.remove(next_step)
        order.append(next_step)
    return order

def get_time_for_step(step):
    return 60 + ord(step) - ord('A')

def get_total_time(dependencies):
    dependencies, working_on, ticks = deepcopy(dependencies), [None] * 5, 0
    while dependencies or not all(job is None for job in working_on):

        for i, job in enumerate(working_on):
            if job and job[1] == 0:
                working_on[i] = None
                for v in (v for v in dependencies.values() if job[0] in v):
                    v.remove(job[0])
            elif job:
                job[1] -= 1

        available_steps = sorted((k for k, v in dependencies.items() if not v), reverse=True)
        for i, job in enumerate(working_on):
            if job is None and available_steps:
                next_step = available_steps.pop()
                working_on[i] = [next_step, get_time_for_step(next_step)]
                del dependencies[next_step]

        ticks += 1

    return ticks - 1

dependencies = get_dependencies()
print(''.join(get_order(dependencies)))
print(get_total_time(dependencies))
