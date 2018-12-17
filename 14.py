from time import sleep

RECIPES = 846601

def digits(n):
    return [int(x) for x in str(n)]

def do_iterations(cnt):
    scores = [3, 7]
    elf1, elf2 = 0, 1
    while len(scores) < cnt + 10:
        for score in digits(scores[elf1] + scores[elf2]): scores.append(score)
        elf1 = (elf1 + scores[elf1] + 1) % len(scores)
        elf2 = (elf2 + scores[elf2] + 1) % len(scores)
    return scores

def next_ten_after(n):
    return do_iterations(n)[n:n + 10]

def find_sublist(x, y):
    for i in range(0, len(x) - len(y)):
        if all(x[i + j] == y[j] for j in range(len(y))):
            return i

def search(sequence):
    scores = [3, 7]
    elf1, elf2 = 0, 1
    prev_length, found_idx = 0, None
    while found_idx is None:

        offset = max(0, prev_length - 5)
        found_idx = find_sublist(scores[offset:], sequence)
        if found_idx is not None: found_idx += offset

        prev_length = len(scores)
        for score in digits(scores[elf1] + scores[elf2]): scores.append(score)
        elf1 = (elf1 + scores[elf1] + 1) % len(scores)
        elf2 = (elf2 + scores[elf2] + 1) % len(scores)

    return found_idx

print(''.join(str(x) for x in next_ten_after(RECIPES)))
print(search(digits(RECIPES)))