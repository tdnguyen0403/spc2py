#!/usr/bin/env python3

from .spc import SPC


class Rules(object):

    def __init__(self, rules='BASIC'):
        self.layers = self
        self.rules = rules

        # default : BASIC
        if rules.lower() == 'basic':
            self.rules = [self.RULE_7_ON_ONE_SIDE,
                          self.RULE_1_BEYOND_3SIGMA]
        # WECO

    #        if rules == 2:
    #            self.rules = [self.RULES_1_BEYOND_3SIGMA,
    #                          self.RULES_2_OF_3_BEYOND_2SIGMA,
    #                          self.RULES_4_OF_5_BEYOND_1SIGMA,
    #                          self.RULES_8_ON_ONE_SIDE,
    #                          self.RULES_6_TRENDING, RULES_14_UP_DOWN]

    def __radd__(self, model):
        if isinstance(model, SPC):
            model.points = self.layers
            return model

        # self.layers.append(model)
        # return self

    @staticmethod
    def test_violating_runs(data, center, lcl, ucl):
        for i in range(1, len(data)):
            if (data[i - 1] - center) * (data[i] - center) < 0:
                return False
        return True

    @staticmethod
    def test_beyond_limits(value, lcl, ucl):
        return value > ucl or value < lcl

    def RULE_1_BEYOND_3SIGMA(self, ax, values, center, lcl, ucl):
        points = []
        if isinstance(lcl, list) and isinstance(ucl, list):
            for i, value in enumerate(values):
                if self.test_beyond_limits(value, lcl[i], ucl[i]):
                    ax.plot([i], value, 'rs', markersize=5)
                    # ax.annotate('%.2f' % value, xy=[i,value], xytext=[-5,10],
                    #     textcoords='offset points')
                    points.append(i)

        elif isinstance(values[0], list):
            for i in range(len(values)):
                for j, value in enumerate(values[i]):
                    if self.test_beyond_limits(value, lcl, ucl):
                        ax.plot([j], value, 'rs', markersize=5)
                        # ax.annotate('%.2f' % value, xy=[j,value], xytext=[-5,10],
                        #     textcoords='offset points')
                        points.append(j)
        else:
            for i in range(len(values)):
                if self.test_beyond_limits(values[i], lcl, ucl):
                    ax.plot([i], values[i], 'rs', markersize=5)
                    # ax.annotate('%.2f' % values[i], xy=[i,values[i]], xytext=[-5,10],
                    #     textcoords='offset points')
                    points.append(i)

        return points

    def RULE_7_ON_ONE_SIDE(self, ax, values, center, lcl, ucl):
        points = []
        # ewma, p Charts
        if isinstance(lcl, list) or isinstance(values[0], list):
            return points
        # mewma Chart
        if center == 0:
            return points

        num = 7
        for i in range(len(values)):
            if i <= (num - 1):
                continue
            if self.test_violating_runs(values[i - num + 1:i + 1], center, lcl, ucl):
                ax.plot([i], values[i], 'rs', markersize=5)
                points.append(i)

        return points

    def plot_violation_points(self, ax, values, center, lcl, ucl):
        violating_points = []
        for func in self.rules:
            violating_points += func(ax, values, center, lcl, ucl)
        return list(set(violating_points))
