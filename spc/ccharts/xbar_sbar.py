import numpy as np

from .ccharts import CCharts
from .tables import A3, B3, B4


class Xbar_Sbar(CCharts):
    _title = "Xbar-S Chart"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(Xbar_Sbar, self).__init__()

    def plot(self, data, size):
        if not hasattr(self, 'transform'):
            assert size >= 10

        # transform the data if required
        if hasattr(self, 'transform'):
            if self.transform == 'split':
                if hasattr(self, 'split_size'):
                    data = self.split_fix(data, self.split_size)
                else:
                    data = self.split_var(data, size)
            else:
                raise ValueError('No such transformation available')

        x, s = [], []
        for xs in data:
            if hasattr(self, 'transform'):
                size = len(xs)
            else:
                assert size == len(xs)
            s.append(np.std(xs, ddof=1))
            x.append(np.mean(xs))

        sbar = np.mean(s)
        xbar = np.mean(x)
        sigma_within = A3[size] * sbar
        sigma_between = self.sigma_between(x, sigma_within, size)
        if hasattr(self, 'calc_method'):
            if self.calc_method == 'standard':
                lcl = xbar - A3[size] * sbar
                ucl = xbar + A3[size] * sbar
            elif self.calc_method == 'extended':
                lcl = xbar - A3[size] * sbar - 1.2 * sigma_between
                ucl = xbar + A3[size] * sbar + 1.2 * sigma_between
        else:
            lcl = xbar - A3[size] * sbar
            ucl = xbar + A3[size] * sbar

        return x, xbar, lcl, ucl, self._title


class Sbar(CCharts):
    _title = "Standard Deviation Chart"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(Sbar, self).__init__()

    def plot(self, data, size):
        if not hasattr(self, 'transform'):
            assert size >= 10

        # transform the data if required
        if hasattr(self, 'transform'):
            if self.transform == 'split':
                if hasattr(self, 'split_size'):
                    data = self.split_fix(data, self.split_size)
                else:
                    data = self.split_var(data, size)
            else:
                raise ValueError('No such transformation available')
        s = []
        for xs in data:
            if hasattr(self, 'transform'):
                size = len(xs)
            else:
                assert size == len(xs)
            s.append(np.std(xs, ddof=1))

        sbar = np.mean(s)

        lcls = B3[size] * sbar
        ucls = B4[size] * sbar

        return s, sbar, lcls, ucls, self._title
