import unittest

from twelve_men_on_an_island import solver
from twelve_men_on_an_island.model import WeightedMan
from twelve_men_on_an_island.scale import Scale, ScaleResult, WeightAnomaly


class TestScale(unittest.TestCase):
    def test_left_heavier(self):
        left = [WeightedMan(0), WeightedMan(1)]
        right = [WeightedMan(2), WeightedMan(3)]
        scale = Scale(0, WeightAnomaly.Heavy)
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.LeftHeavier, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_left_lighter(self):
        left = [WeightedMan(0), WeightedMan(1)]
        right = [WeightedMan(2), WeightedMan(3)]
        scale = Scale(1, WeightAnomaly.Light)
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.RightHeavier, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_right_heavier(self):
        left = [WeightedMan(0), WeightedMan(1)]
        right = [WeightedMan(2), WeightedMan(3)]
        scale = Scale(3, WeightAnomaly.Heavy)
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.RightHeavier, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_right_lighter(self):
        left = [WeightedMan(0), WeightedMan(1)]
        right = [WeightedMan(2), WeightedMan(3)]
        scale = Scale(2, WeightAnomaly.Light)
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.LeftHeavier, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_equal(self):
        scale = Scale(-1, None)
        left = [WeightedMan(0), WeightedMan(1)]
        right = [WeightedMan(2), WeightedMan(3)]
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.Equal, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_weight_counter(self):
        left = [WeightedMan(0), WeightedMan(1)]
        right = [WeightedMan(2), WeightedMan(3)]
        another = [WeightedMan(4), WeightedMan(5)]
        scale = Scale(2, WeightAnomaly.Light)
        scale.compare(left, right)
        scale.compare(right, left)
        scale.compare(left, another)
        scale.compare(another, right)
        self.assertEqual(4, scale.get_weight_count())


def simple_list():
    return [WeightedMan(i+1) for i in range(12)]


class TestSolver(unittest.TestCase):
    def __test_nth(self, i, new_weight):
        scale = Scale(i, new_weight)
        list_o_men = simple_list()
        result = solver.solve(list_o_men, scale)
        self.assertEqual(i, result[0].id)
        self.assertEqual(new_weight, result[1])
        self.assertLessEqual(scale.get_weight_count(), 3)

    def test_01_heavier(self):
        self.__test_nth(1, WeightAnomaly.Heavy)

    def test_01_lighter(self):
        self.__test_nth(1, WeightAnomaly.Light)

    def test_02_heavier(self):
        self.__test_nth(2, WeightAnomaly.Heavy)

    def test_02_lighter(self):
        self.__test_nth(2, WeightAnomaly.Light)

    def test_03_heavier(self):
        self.__test_nth(3, WeightAnomaly.Heavy)

    def test_03_lighter(self):
        self.__test_nth(3, WeightAnomaly.Light)

    def test_04_heavier(self):
        self.__test_nth(4, WeightAnomaly.Heavy)

    def test_04_lighter(self):
        self.__test_nth(4, WeightAnomaly.Light)

    def test_05_heavier(self):
        self.__test_nth(5, WeightAnomaly.Heavy)

    def test_05_lighter(self):
        self.__test_nth(5, WeightAnomaly.Light)

    def test_06_heavier(self):
        self.__test_nth(6, WeightAnomaly.Heavy)

    def test_06_lighter(self):
        self.__test_nth(6, WeightAnomaly.Light)

    def test_07_heavier(self):
        self.__test_nth(7, WeightAnomaly.Heavy)

    def test_07_lighter(self):
        self.__test_nth(7, WeightAnomaly.Light)

    def test_08_heavier(self):
        self.__test_nth(8, WeightAnomaly.Heavy)

    def test_08_lighter(self):
        self.__test_nth(8, WeightAnomaly.Light)

    def test_09_heavier(self):
        self.__test_nth(9, WeightAnomaly.Heavy)

    def test_09_lighter(self):
        self.__test_nth(9, WeightAnomaly.Light)

    def test_10_heavier(self):
        self.__test_nth(10, WeightAnomaly.Heavy)

    def test_10_lighter(self):
        self.__test_nth(10, WeightAnomaly.Light)

    def test_11_heavier(self):
        self.__test_nth(11, WeightAnomaly.Heavy)

    def test_11_lighter(self):
        self.__test_nth(11, WeightAnomaly.Light)

    def test_12_heavier(self):
        self.__test_nth(12, WeightAnomaly.Heavy)

    def test_12_lighter(self):
        self.__test_nth(12, WeightAnomaly.Light)


if __name__ == '__main__':
    unittest.main()
