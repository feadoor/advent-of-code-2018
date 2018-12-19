from math import sqrt

def sum_of_divisors(n):
    limit = int(sqrt(n))
    return (limit if n % limit == 0 else 0) + sum(x + n // x for x in filter(lambda x: n % x == 0, range(1, limit)))

print(sum_of_divisors(986))
print(sum_of_divisors(10551386))