import random


RANGE = [0, 1]


def expand(i):
    assert i in RANGE
    return (i*2) - 1

def simulate_single_scenario(size):
    # cheaters_map = {}
    cheated_from = {}
    for i in range(size):
        direction = expand(random.randint(0, 1))
        # cheaters_map[i] = direction
        cheated_from[(i + direction) % size] = 1
    # print ""
    # print cheaters_map
    return cheated_from.keys()


def simulate(size=8, number_of_simulations=100):
    acc = 0.0
    for i in range(number_of_simulations):
        result = simulate_single_scenario(size)
        score = size - len(result)
        acc += score
        print score, '->', (acc)/(i+1)
    print float(size)/4


simulate(8, 10000)

