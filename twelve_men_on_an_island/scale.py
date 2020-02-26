from enum import Enum


class WeightAnomaly(Enum):
    Light = 0
    Heavy = 1


class ScaleResult(Enum):
    LeftHeavier = 1
    Equal = 2
    RightHeavier = 3


class Scale(object):
    def __init__(self, anlomaly_id, anomaly_weight):
        self.__count = 0
        self.__anomaly_id = anlomaly_id
        self.__anomaly_weight = anomaly_weight

    def compare(self, left_list, right_list):
        if len(left_list) != len(right_list):
            raise RuntimeError("weighted lists have different size")
        self.__count = self.__count + 1
        if any(man.id == self.__anomaly_id for man in left_list):
            return ScaleResult.LeftHeavier if self.__anomaly_weight == WeightAnomaly.Heavy else ScaleResult.RightHeavier
        if any(man.id == self.__anomaly_id for man in right_list):
            return ScaleResult.RightHeavier if self.__anomaly_weight == WeightAnomaly.Heavy else ScaleResult.LeftHeavier
        else:
            return ScaleResult.Equal

    def get_weight_count(self):
        return self.__count
