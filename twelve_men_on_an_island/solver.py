from enum import Enum

from twelve_men_on_an_island.scale import ScaleResult, WeightAnomaly


class ScaleSide(Enum):
    L = 0
    R = 1
    N = 2


class WeighingResult(Enum):
    H = 1
    L = 2
    E = 0
    X = 3


class SolvedMan(object):
    def __init__(self, man, weighing_scheme):
        self.__man = man
        self.__weighing_scheme = weighing_scheme
        self.__measurements = list()

    def __repr__(self):
        return str(self.__man.id) + " " +\
               str(self.__weighing_scheme) + ' ' +\
               str(self.__measurements)

    def get_weighing_scheme(self):
        return self.__weighing_scheme

    def get_weighing_position(self, index):
        return self.__weighing_scheme[index]

    def get_man(self):
        return self.__man

    def add_weighing_result(self, measurement):
        self.__measurements.append(measurement)

    def has_all_outlying_results(self):
        return any(
            [
                all(map(lambda mes: mes in [WeighingResult.L, WeighingResult.X], self.__measurements)),
                all(map(lambda mes: mes in [WeighingResult.H, WeighingResult.X], self.__measurements))
            ]
        )

    def derive_weight(self):
        if all(map(lambda mes: mes in [WeighingResult.L, WeighingResult.X], self.__measurements)):
            return WeightAnomaly.Light
        elif all(map(lambda mes: mes in [WeighingResult.H, WeighingResult.X], self.__measurements)):
            return WeightAnomaly.Heavy
        if self.has_all_outlying_results() :
            return WeightAnomaly.Normal



### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###
### ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### ---


MAGIC_ENCODING = {
    0: [0, 0, 0],
    1: [0, 0, 1],
    2: [0, 1, 1],
    3: [0, 1, 2],
    4: [1, 1, 2],
    5: [1, 2, 0],
    6: [1, 2, 1],
    7: [1, 2, 2],
    8: [2, 0, 0],
    9: [2, 1, 0],
    10: [2, 0, 2],
    11: [2, 2, 1]
}


def encode12(i):
    return tuple(map(lambda n: ScaleSide(n), MAGIC_ENCODING[i]))
    # return (
    #     ScaleSide((i // 4) % 3),
    #     ScaleSide((i // 2) % 3),
    #     ScaleSide((i // 1) % 3)
    # )


def assert_uniq(_list):
    _set = set(_list)
    assert len(_set) == len(_list)


def assign_with_weighing_scheme(list_of_men):
    solvable_men = list()
    for i in range(len(list_of_men)):
        encode_ = encode12(i)
        newman = SolvedMan(list_of_men[i], encode_)
        solvable_men.append(newman)
    assert_uniq(list(map(SolvedMan.get_weighing_scheme, solvable_men)))
    return solvable_men


SCALE_RESULT_MAPPING = {
    (ScaleResult.LeftHeavier, ScaleSide.L): WeighingResult.H,
    (ScaleResult.LeftHeavier, ScaleSide.R): WeighingResult.L,
    (ScaleResult.LeftHeavier, ScaleSide.N): WeighingResult.E,

    (ScaleResult.RightHeavier, ScaleSide.L): WeighingResult.L,
    (ScaleResult.RightHeavier, ScaleSide.R): WeighingResult.H,
    (ScaleResult.RightHeavier, ScaleSide.N): WeighingResult.E,

    (ScaleResult.Equal, ScaleSide.L): WeighingResult.E,
    (ScaleResult.Equal, ScaleSide.R): WeighingResult.E,
    (ScaleResult.Equal, ScaleSide.N): WeighingResult.X,
}


def scale_result_mapping(scale_result, scale_side):
    return SCALE_RESULT_MAPPING.get((scale_result, scale_side))


def compare_weights(scale, left_side, right_side):
    return scale.compare(extract_man(left_side), extract_man(right_side))


def extract_man(left_side):
    return list(map(SolvedMan.get_man, left_side))


def perform_weighing(scale, solvable_men):
    for weighing_attempt in range(3):
        left_side = list(filter(lambda m: m.get_weighing_position(weighing_attempt) == ScaleSide.L, solvable_men))
        right_side = list(filter(lambda m: m.get_weighing_position(weighing_attempt) == ScaleSide.R, solvable_men))
        remainder = list(filter(lambda m: m.get_weighing_position(weighing_attempt) == ScaleSide.N, solvable_men))
        result = compare_weights(scale, left_side, right_side)
        for man in left_side:
            man.add_weighing_result(scale_result_mapping(result, ScaleSide.L))
        for man in right_side:
            man.add_weighing_result(scale_result_mapping(result, ScaleSide.R))
        for man in remainder:
            man.add_weighing_result(scale_result_mapping(result, ScaleSide.N))


def find_men_with_consistent_measurements(solvable_men):
    return list(filter(SolvedMan.has_all_outlying_results, solvable_men))


def solve_with_mapping(list_of_men, scale):
    assert len(list_of_men) == 12
    solvable_men = assign_with_weighing_scheme(list_of_men)
    perform_weighing(scale, solvable_men)
    outliers = find_men_with_consistent_measurements(solvable_men)
    assert len(outliers) == 1
    the_man = outliers[0]
    return the_man.get_man(), the_man.derive_weight()


### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###
### ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### ---


def sublist(the_list, indices):
    return [the_list[i-1] for i in indices]


def compare_sublists(scale, list_, left_i, right_i):
    left_side = sublist(list_, left_i)
    right_side = sublist(list_, right_i)
    result = scale.compare(left_side, right_side)
    # print(left_side,  "vs", fascists, '->', result)
    return result


def pick(list_, natural_index):
    return list_[natural_index-1]


def solve_with_logic(list_of_men, scale):
    result = compare_sublists(scale, list_of_men, [1, 2, 3, 4], [5, 6, 7, 8])
    if result == ScaleResult.Equal:
        result = compare_sublists(scale, list_of_men, [9], [10])
        if result == ScaleResult.Equal:
            result = compare_sublists(scale, list_of_men, [9], [11])
            if result == ScaleResult.Equal:
                return pick(list_of_men, 12),
            else:
                return pick(list_of_men, 11)
        else:
            result = compare_sublists(scale, list_of_men, [9], [11])
            if result == ScaleResult.Equal:
                return pick(list_of_men, 10)
            else:
                return pick(list_of_men, 9)

    elif result == ScaleResult.LeftHeavier:
        result = compare_sublists(scale, list_of_men, [1, 2, 3, 5], [4, 10, 11, 12])
        if result == ScaleResult.LeftHeavier:
            result = compare_sublists(scale, list_of_men, [1], [2])
            if result == ScaleResult.LeftHeavier:
                return pick(list_of_men, 1)
            elif result == ScaleResult.RightHeavier:
                return pick(list_of_men, 2)
            else:
                return pick(list_of_men, 3)
        elif result == ScaleResult.RightHeavier:
            result = compare_sublists(scale, list_of_men, [4], [12])
            if result == ScaleResult.Equal:
                return pick(list_of_men, 5)
            else:
                return pick(list_of_men, 4)
        else:
            result = compare_sublists(scale, list_of_men, [6], [7])
            if result == ScaleResult.LeftHeavier:
                return pick(list_of_men, 7)
            elif result == ScaleResult.RightHeavier:
                return pick(list_of_men, 6)
            else:
                return pick(list_of_men, 8)

    elif result == ScaleResult.RightHeavier:
        result = compare_sublists(scale, list_of_men, [5, 10, 11, 12], [4, 6, 7, 8])
        if result == ScaleResult.RightHeavier:
            result = compare_sublists(scale, list_of_men, [6], [7])
            if result == ScaleResult.RightHeavier:
                return pick(list_of_men, 7)
            elif result == ScaleResult.LeftHeavier:
                return pick(list_of_men, 6)
            else:
                return pick(list_of_men, 8)
        elif result == ScaleResult.LeftHeavier:
            result = compare_sublists(scale, list_of_men, [5], [12])
            if result == ScaleResult.Equal:
                return pick(list_of_men, 4)
            else:
                return pick(list_of_men, 5)
        else:
            result = compare_sublists(scale, list_of_men, [1], [2])
            if result == ScaleResult.RightHeavier:
                return pick(list_of_men, 1)
            elif result == ScaleResult.LeftHeavier:
                return pick(list_of_men, 2)
            else:
                return pick(list_of_men, 3)

    raise RuntimeError("This should not happen")


### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###
### ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### ---


def solve(list_of_men, scale):
    return solve_with_mapping(list_of_men, scale)
    #
    # solution = solve_with_logic(list_of_men, scale)
    # return (solution.get_man(), solution.get_man().weight)
