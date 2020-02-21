from enum import Enum


class ScaleSide(Enum):
    L = 0
    R = 1
    N = 2


class ScaleResult(Enum):
    H = 1
    L = 2
    E = 0
    X = 3


class SolvedMan(object):
    def __init__(self, man, weighting_order):
        self.__man = man
        self.__weighting_order = weighting_order

    def get_side_for_wrighing(self, index):
        return self.__weighting_order[index]


def encode12(i):
    return (
        ScaleSide((i // 4) % 3),
        ScaleSide((i // 2) % 3),
        ScaleSide((i // 1) % 3)
    )


def assert_uniq(l):
    s = set(l)
    assert len(s) == len(l)


def solve12(list_of_men, scale):
    for i in range(len(list_of_men)):
        encode12(i)
    encoded_sides = list(map(lambda index: SolvedMan(list_of_men[index], encode12(index)), range(len(list_of_men))))
    # for i in encoded_sides:
    #     print(i)
    assert_uniq(encoded_sides)

    return list_of_men[0]


def solve27(list_of_men, scale):
    return list_of_men[0]


def solve(list_of_men, scale):
    if len(list_of_men) == 12:
        return solve12(list_of_men, scale)
    if len(list_of_men) == 27:
        return solve27(list_of_men, scale)
    raise RuntimeError("unsupported list length: " + len(list_of_men))

