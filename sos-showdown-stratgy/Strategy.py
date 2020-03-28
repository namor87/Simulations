from enum import Enum
# from puffadder import *
# from numbers import


# @contructor
class Strategy (Enum):
    # pass
    def __init__(self, L1, L2, L3):
        self.__L2 = L2
        self.__L3 = L3
        self.__L1 = L1
        assert L1 + L2 + L3 == 12


class Formation (Strategy):
    pass;


class Match (object):
    def __init__(self, S1, S2):
        self.__S1 = S1
        self.__S2 = S2
        assert type(S1) == Strategy
        assert type(S2) == Strategy








