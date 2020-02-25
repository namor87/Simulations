from enum import Enum

from twelve_men_on_an_island.model import Weight


class ScaleResult(Enum):
    LeftHeavier = 1
    Equal = 2
    RightHeavier = 3


class Scale(object):
    def __init__(self):
        self.__count = 0

    def compare(self, left_list, right_list):
        if len(left_list) != len(right_list):
            raise RuntimeError("weighted lists have different size")
        left_abnormal = self.find_different_weights(left_list)
        right_abnormal = self.find_different_weights(right_list)
        if len(left_abnormal + right_abnormal) > 1:
            raise RuntimeError("too many abnormal weights in two lists. only one expected")
        self.__count = self.__count + 1
        if len(left_abnormal) == 1:
            return ScaleResult.LeftHeavier if left_abnormal[0].weight == Weight.Heavy else ScaleResult.RightHeavier
        if len(right_abnormal) == 1:
            return ScaleResult.RightHeavier if right_abnormal[0].weight == Weight.Heavy else ScaleResult.LeftHeavier
        return ScaleResult.Equal

    def get_weight_count(self):
        return self.__count

    @staticmethod
    def find_different_weights(people_list):
        return list(filter(lambda x: x.weight != Weight.Normal, people_list))
