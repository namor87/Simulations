import enum


class Weight(enum.Enum):
    Light = 0
    Normal = 1
    Heavy = 2


class WeightedMan(object):
    def __init__(self, id, weight):
        assert type(weight) == Weight
        self.id = id
        self.weight = weight

    def __repr__(self):
        return str(self.id) + ":" + str(self.weight.name)
