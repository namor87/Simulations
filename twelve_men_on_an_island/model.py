import enum


class WeightedMan(object):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return str(self.id)
