def parse_freq(freq):
    if freq[0] == '-':
        return -int(freq[1:])
    else:
        return int(freq[1:])

def get_frequencies():
    with open('data/1.txt', 'r') as f:
        return [parse_freq(freq) for freq in f]

def get_total_freq(freqs):
    return sum(freqs)

def get_first_repeat(freqs):
    total, seen, idx = 0, set(), 0

    while total not in seen:
        seen.add(total)
        total += freqs[idx]
        idx = idx + 1 if idx < len(freqs) - 1 else 0

    return total

freqs = get_frequencies()
print(get_total_freq(freqs))
print(get_first_repeat(freqs))