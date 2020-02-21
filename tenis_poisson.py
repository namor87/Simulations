from math import pow

integrals = [1, 1]


def integral(n):
    assert n >= 0
    last_index = len(integrals) - 1
    if last_index >= n:
        return integrals[n]
    else:
        next_value = integrals[last_index] * (last_index+1)
        integrals.append(next_value)
        return integral(n)


def newton(n, k):
    assert n >= 0
    assert k >= 0
    assert n >= k
    return integral(n) / (integral(k) * integral(n - k))


def probability_of_victory(p, n):
    assert p > 0.0
    assert p < 1.0
    flawless_victory = pow(p, n)
    pp = 1.0 - p
    exponents = range(n)
    powers_of_probability = map(lambda k: pow(pp, k) * newton(n + k - 1, k), exponents)
    return flawless_victory * sum(powers_of_probability)


def compare(prop, points, sets):
    global p_long_match, px2
    p_set = probability_of_victory(prop, points)
    p_set_match = probability_of_victory(p_set, sets)
    p_long_match = probability_of_victory(prop, points * sets)
    # print points, 'x', sets,  p_set_match , p_long_match, p_set_match - p_long_match
    print "%02dx%02d"%(points, sets),  p_set_match - p_long_match


p = 0.55
compare(p, 2, 12)
compare(p, 3, 8)
compare(p, 4, 6)
compare(p, 5, 5)
compare(p, 6, 4)
compare(p, 8, 3)
compare(p, 12, 2)


