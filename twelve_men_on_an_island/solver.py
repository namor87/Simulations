from enum import Enum

from twelve_men_on_an_island.scale import ScaleResult


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
               str(self.__man.weight) + ' ' +\
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
    return outliers[0].get_man()


### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###
### ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### ---


def test_3_with_2_weighings():
    pass


def solve_with_logic():
    pass


### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###
### ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### ---


def solve(list_of_men, scale):
    return solve_with_mapping(list_of_men, scale)
