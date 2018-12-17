from collections import defaultdict
from operator import itemgetter
import re

START_SHIFT = 'SHIFT'
AWAKE = 'AWAKE'
ASLEEP = 'ASLEEP'

entry_regex = re.compile('\[1518-(\d\d)-(\d\d)\ (\d\d):(\d\d)] (?:Guard #(\d+) begins shift|(falls asleep)|(wakes up))')

class Entry:

    def __init__(self, entry):
        match = entry_regex.match(entry)

        self.month = int(match.group(1))
        self.day = int(match.group(2))
        self.hour = int(match.group(3))
        self.minute = int(match.group(4))

        if match.group(6) == 'falls asleep':
            self.type = ASLEEP
        elif match.group(7) == 'wakes up':
            self.type = AWAKE
        else:
            self.id = int(match.group(5))
            self.type = START_SHIFT

    def __lt__(self, other):
        self_tuple = (self.month, self.day, self.hour, self.minute)
        other_tuple = (other.month, other.day, other.hour, other.minute)
        return self_tuple < other_tuple


def get_data():
    with open('data/4.txt', 'r') as f:
        return sorted(Entry(line) for line in f)

def get_total_sleep_by_guard(data):
    total_sleep, minutes_asleep = defaultdict(int), defaultdict(lambda: defaultdict(int))
    active_guard, sleep_start = None, None

    for entry in data:
        if entry.type == START_SHIFT:
            active_guard = entry.id
        elif entry.type == ASLEEP:
            sleep_start = entry.minute
        elif entry.type == AWAKE:
            total_sleep[active_guard] += entry.minute - sleep_start
            for minute in range(sleep_start, entry.minute):
                minutes_asleep[active_guard][minute] += 1

    return (total_sleep, minutes_asleep)

def get_total_sleep_by_minute(data):
    sleep_by_minute = defaultdict(lambda: defaultdict(int))
    active_guard, sleep_start = None, None

    for entry in data:
        if entry.type == START_SHIFT:
            active_guard = entry.id
        elif entry.type == ASLEEP:
            sleep_start = entry.minute
        elif entry.type == AWAKE:
            for minute in range(sleep_start, entry.minute):
                sleep_by_minute[minute][active_guard] += 1

    return sleep_by_minute


def strategy1(data):
    total_sleep, minutes_asleep = get_total_sleep_by_guard(data)
    best_guard = max(total_sleep.items(), key=itemgetter(1))[0]
    best_minute = max(minutes_asleep[best_guard].items(), key=itemgetter(1))[0]
    return best_guard * best_minute

def strategy2(data):
    sleep_by_minute = get_total_sleep_by_minute(data)
    best_per_minute = {m : max(sleep_by_minute[m].items(), key=itemgetter(1)) for m in sleep_by_minute.keys()}
    best_entry = max(best_per_minute.items(), key=lambda kv: kv[1][1])
    best_minute, best_guard = best_entry[0], best_entry[1][0]
    return best_minute * best_guard

data = get_data()
print(strategy1(data))
print(strategy2(data))
