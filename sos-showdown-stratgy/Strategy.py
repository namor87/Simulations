import itertools
import os


class Formation:
    def __init__(self, L1, L2, L3):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        assert L1 + L2 + L3 == 12

    def __repr__(self):
        return str([self.L1, self.L2, self.L3])


class Strategy:
    def __init__(self, name, L1, L2, L3):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.name = name
        assert L1 + L2 + L3 == 12

    def __repr__(self):
        return self.name + ':' + str([self.L1, self.L2, self.L3])

    def base_formation(self):
        return Formation(self.L1, self.L2, self.L3)

    def all_possible_formations(self):
        lines_permutations = itertools.permutations([self.L1, self.L2, self.L3])
        return map(lambda lines: Formation(lines[0], lines[1], lines[2]), lines_permutations)


class MatchScore:
    def __init__(self, left_score, right_score,):
        self.left_score = left_score
        self.right_score = right_score

    def __repr__(self):
        scorelist = (self.left_score, self.right_score)
        return str(list(map(lambda x: round(x, 2), scorelist)))


class Match(object):
    def __init__(self, F1, F2):
        self.__F1 = F1
        self.__F2 = F2
        assert isinstance(F1, Formation)
        assert isinstance(F2, Formation)

    def calculate(self):
        lane_1_score = self.__compare(self.__F1.L1, self.__F2.L1)
        lane_2_score = self.__compare(self.__F1.L2, self.__F2.L2)
        lane_3_score = self.__compare(self.__F1.L3, self.__F2.L3)
        f1_flags = lane_1_score + lane_2_score + lane_3_score
        return MatchScore(f1_flags, 3.0 - f1_flags)

    def __compare(self, lane1, lane2):
        return 1 if lane1 > lane2 else 0 if lane1 < lane2 else 0.5


class ScoreRecord:
    def __init__(self, left_score, left_flags, left_points, right_score, right_flags, right_points):
        self.left_score = left_score
        self.left_flags = left_flags
        self.left_points = left_points
        self.right_score = right_score
        self.right_flags = right_flags
        self.right_points = right_points

    def reverse(self):
        return ScoreRecord(self.right_score, self.right_flags, self.right_points, self.left_score, self.left_flags, self.left_points)

    def __repr__(self):
        s = (self.left_score, self.right_score, self.left_points, self.right_points, self.left_flags, self.right_flags)
        return "[%.1f-%.1f (%.1f-%.1f) %.0f%%]" % (s[2], s[3], s[4], s[5], s[0]*100)


class StrategyCompare:
    def __init__(self, S1, S2):
        self.S1 = S1
        self.S2 = S2

    def evaluate(self):
        left_score, left_points, left_flags, right_score,right_points, right_flags = 0, 0, 0, 0, 0, 0
        count = 0
        right_formation = self.S2.base_formation()
        for formation in self.S1.all_possible_formations():
            count = count + 1
            scoreboard = Match(formation, right_formation).calculate()
            left_w, right_w = self.__map_wins(scoreboard)
            left_p, right_p = self.__map_points(scoreboard)
            left_score, right_score = left_score + left_w, right_score + right_w
            left_points, right_points = left_points + left_p, right_points + right_p
            left_flags, right_flags = left_flags + scoreboard.left_score, right_flags + scoreboard.right_score

        return ScoreRecord(
            left_score/count,
            left_flags/count,
            left_points/count,
            right_score/count,
            right_flags/count,
            right_points/count)

    @staticmethod
    def __map_wins(scoreboard):
        return (1, 0) if scoreboard.left_score > scoreboard.right_score \
            else (0, 1) if scoreboard.left_score < scoreboard.right_score \
            else (0.5, 0.5)

    @staticmethod
    def __map_points(scoreboard):
        return (3, 0) if scoreboard.left_score > scoreboard.right_score \
            else (0, 3) if scoreboard.left_score < scoreboard.right_score \
            else (1, 1)


class StrategyScore:
    def __init__(self, strategy, score_dict):
        self.strategy = strategy
        self.score_dict = score_dict
        self.avg_wins = self.average_of(lambda scoreboard: scoreboard.left_score)
        self.avg_points = self.average_of(lambda scoreboard: scoreboard.left_points)
        self.avg_flags = self.average_of(lambda scoreboard: scoreboard.left_flags)

    def average_of(self, map_selector):
        values_map = map(map_selector, self.score_dict.values())
        average = sum(values_map) / len(self.score_dict)
        return round(average, 2)

    def print_short(self):
        scores_str = ' | '.join(map(lambda x: str(round(x, 1)), (self.avg_points, self.avg_flags, self.avg_wins)))
        return "%30s --  %s" % (str(self.strategy), scores_str)

    @staticmethod
    def print_result(other_strategy, score_board):
        return str(other_strategy) + " - " + str(score_board)

    def print_long(self):
        sep = os.linesep + '\t'
        return self.print_short().strip() + sep + \
               sep.join(map(lambda element: self.print_result(element[0], element[1]), self.score_dict.items()))


class Accounting:
    scores = dict()

    def register(self, strategy, against, score):
        if strategy in self.scores:
            self.scores[strategy][against] = score
        else:
            self.scores[strategy] = {against: score}

    def sumup(self):
        return list(map(lambda entry: StrategyScore(entry[0], entry[1]), self.scores.items()))


# # # # #   MAIN   # # # # #


strategies = [
    Strategy('EQUAL_TOP', 6, 6, 0),
    Strategy('EQUAL_ALL', 4, 4, 4),
    Strategy('EQUAL_BOTTOM', 8, 2, 2),
    Strategy('SEQUENTIAL', 6, 4, 2),
    Strategy('SEQUENTIAL_LIGHT', 5, 4, 3),
    Strategy('SEQUENTIAL_MAX', 8, 4, 0)
]

account = Accounting()


for (strategy_one, strategy_two) in itertools.combinations(strategies, 2):
    score = StrategyCompare(strategy_one, strategy_two).evaluate()
    account.register(strategy_one, strategy_two, score)
    account.register(strategy_two, strategy_one, score.reverse())

sorted_scores = account.sumup()

sorted_scores.sort(key=lambda ss: (ss.avg_points, ss.avg_wins), reverse=True)

for strategy_score in sorted_scores:
    # print(strategy_score.print_short())
    print(strategy_score.print_long())
