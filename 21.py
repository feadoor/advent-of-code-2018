def mutilate(r2, r3, r5):
        r3 = r5 & 255
        r2 = r2 + r3
        r2 &= 16777215
        r2 *= 65899
        r2 &= 16777215
        return r2, r3, r5

def quickest_r0():
    r2, r3, r5 = 2238642, 0, 65536
    while r5 > 0:
        r2, r3, r5 = mutilate(r2, r3, r5)
        r5 //= 256
    return r2

def slowest_r0():

    last_r2, seen_r5s = None, set()
    r2, r3, r5 = 0, 0, 0

    while True:
        r5, r2 = r2 | 65536, 2238642
        if r5 in seen_r5s:
            return last_r2

        starting_r5 = r5

        while r5 > 0:
            r2, r3, r5 = mutilate(r2, r3, r5)
            r5 //= 256

        seen_r5s.add(starting_r5)
        last_r2 = r2

print(quickest_r0())
print(slowest_r0())
