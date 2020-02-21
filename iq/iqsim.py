import random


SIZE = 10000000

MEAN = 100
VAR = 15

#SHIFT = VAR


def test(population, threshold):
    return len(filter(lambda x: x >= threshold, population))


def main():
    pop = [random.normalvariate(MEAN, VAR) for _ in range(SIZE)]
    popA = [random.normalvariate(MEAN + VAR, VAR) for _ in range(SIZE)]
    for i in (115, 130, 145, 160, 175, 190):
        print i, test(pop,i), test(popA,i)


for i in range(1):
    print "--------------------"
    main()

