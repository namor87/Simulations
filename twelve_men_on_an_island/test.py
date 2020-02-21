import unittest
import random

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
        result = scale.compare(left, right)
        result = scale.compare(right, left)
        result = scale.compare(left, another)
        result = scale.compare(another, right)
        self.assertEqual(4, scale.get_weight_count())


def simple_list():
    return [WeightedMan(i, Weight.Normal) for i in range(12)]


class TestSolver(unittest.TestCase):
    def test_simple(self):
        scale = Scale()
        list_o_men = simple_list()
        list_o_men[0].weight = Weight.Heavy
        result = solver.solve(list_o_men, scale)
        self.assertIn(result.weight, [Weight.Heavy, Weight.Light])
        self.assertLessEqual(scale.get_weight_count(), 3)

    def test_random(self):
        scale = Scale()
        list_o_men = simple_list()
        list_o_men[random.randint(0, 11)].weight = Weight.Heavy
        result = solver.solve(list_o_men, scale)
        self.assertIn(result.weight, [Weight.Heavy, Weight.Light])
        self.assertLessEqual(scale.get_weight_count(), 3)

    def test_extensive(self):
        for i in range(12):
            for new_weight in [Weight.Heavy, Weight.Light]:
                scale = Scale()
                list_o_men = simple_list()
                list_o_men[i].weight = new_weight
                result = solver.solve(list_o_men, )
                self.assertEqual(result.weight, new_weight)
                self.assertEqual(result.id, i)
                self.assertLessEqual(scale.get_weight_count(), 3)


if __name__ == '__main__':
    unittest.main()
