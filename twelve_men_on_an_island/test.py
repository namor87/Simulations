import unittest

from twelve_men_on_an_island import solver
from twelve_men_on_an_island.model import WeightedMan, Weight
from twelve_men_on_an_island.scale import Scale, ScaleResult


class TestScale(unittest.TestCase):
    def test_left_heavier(self):
        left = [WeightedMan(0, Weight.Heavy), WeightedMan(1, Weight.Normal)]
        right = [WeightedMan(0, Weight.Normal), WeightedMan(1, Weight.Normal)]
        scale = Scale()
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.LeftHeavier, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_left_lighter(self):
        left = [WeightedMan(0, Weight.Light), WeightedMan(1, Weight.Normal)]
        right = [WeightedMan(0, Weight.Normal), WeightedMan(1, Weight.Normal)]
        scale = Scale()
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.RightHeavier, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_right_heavier(self):
        left = [WeightedMan(0, Weight.Normal), WeightedMan(1, Weight.Normal)]
        right = [WeightedMan(0, Weight.Heavy), WeightedMan(1, Weight.Normal)]
        scale = Scale()
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.RightHeavier, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_right_lighter(self):
        left = [WeightedMan(0, Weight.Normal), WeightedMan(1, Weight.Normal)]
        right = [WeightedMan(0, Weight.Light), WeightedMan(1, Weight.Normal)]
        scale = Scale()
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.LeftHeavier, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_equal(self):
        left = [WeightedMan(0, Weight.Normal), WeightedMan(1, Weight.Normal)]
        right = [WeightedMan(0, Weight.Normal), WeightedMan(1, Weight.Normal)]
        scale = Scale()
        result = scale.compare(left, right)
        self.assertEqual(ScaleResult.Equal, result)
        self.assertEqual(1, scale.get_weight_count())

    def test_weight_counter(self):
        left = [WeightedMan(0, Weight.Normal), WeightedMan(1, Weight.Normal)]
        right = [WeightedMan(0, Weight.Light), WeightedMan(1, Weight.Normal)]
        another = [WeightedMan(0, Weight.Normal), WeightedMan(1, Weight.Normal)]
        scale = Scale()
        scale.compare(left, right)
        scale.compare(right, left)
        scale.compare(left, another)
        scale.compare(another, right)
        self.assertEqual(4, scale.get_weight_count())


def simple_list():
    return [WeightedMan(i+1, Weight.Normal) for i in range(12)]


class TestSolver(unittest.TestCase):
    def __test_nth(self, i, new_weight):
        scale = Scale()
        list_o_men = simple_list()
        list_o_men[i].weight = new_weight
        result = solver.solve(list_o_men, scale)
        self.assertEqual(i+1, result.id)
        self.assertEqual(new_weight, result.weight)
        self.assertLessEqual(scale.get_weight_count(), 3)

    def test_01_heavier(self):
        self.__test_nth(0, Weight.Heavy)

    def test_01_lighter(self):
        self.__test_nth(0, Weight.Light)

    def test_02_heavier(self):
        self.__test_nth(1, Weight.Heavy)

    def test_02_lighter(self):
        self.__test_nth(1, Weight.Light)

    def test_03_heavier(self):
        self.__test_nth(2, Weight.Heavy)

    def test_03_lighter(self):
        self.__test_nth(2, Weight.Light)

    def test_04_heavier(self):
        self.__test_nth(3, Weight.Heavy)

    def test_04_lighter(self):
        self.__test_nth(3, Weight.Light)

    def test_05_heavier(self):
        self.__test_nth(4, Weight.Heavy)

    def test_05_lighter(self):
        self.__test_nth(4, Weight.Light)

    def test_06_heavier(self):
        self.__test_nth(5, Weight.Heavy)

    def test_06_lighter(self):
        self.__test_nth(5, Weight.Light)

    def test_07_heavier(self):
        self.__test_nth(6, Weight.Heavy)

    def test_07_lighter(self):
        self.__test_nth(6, Weight.Light)

    def test_08_heavier(self):
        self.__test_nth(7, Weight.Heavy)

    def test_08_lighter(self):
        self.__test_nth(7, Weight.Light)

    def test_09_heavier(self):
        self.__test_nth(8, Weight.Heavy)

    def test_09_lighter(self):
        self.__test_nth(8, Weight.Light)

    def test_10_heavier(self):
        self.__test_nth(9, Weight.Heavy)

    def test_10_lighter(self):
        self.__test_nth(9, Weight.Light)

    def test_11_heavier(self):
        self.__test_nth(10, Weight.Heavy)

    def test_11_lighter(self):
        self.__test_nth(10, Weight.Light)

    def test_12_heavier(self):
        self.__test_nth(11, Weight.Heavy)

    def test_12_lighter(self):
        self.__test_nth(11, Weight.Light)


if __name__ == '__main__':
    unittest.main()
