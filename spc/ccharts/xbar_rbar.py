import numpy as np

from .ccharts import CCharts
from .tables import A2, D3, D4


class Xbar_Rbar(CCharts):
    _title = "Xbar-R Chart"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(Xbar_Rbar, self).__init__()

    def plot(self, data, size):
        if not hasattr(self, 'transform'):
            assert size >= 2
            assert size < 10

        # transform the data if required
        if hasattr(self, 'transform'):
            if self.transform == 'split':
                if hasattr(self, 'split_size'):
                    data = self.split_fix(data, self.split_size)
                else:
                    data = self.split_var(data, size)
            else:
                raise ValueError('No such transformation available')

        r, x = [], []  # values
        for xs in data:
            if hasattr(self, 'transform'):
                size = len(xs)
            else:
                assert size == len(xs)
            r.append(max(xs) - min(xs))
            x.append(np.mean(xs))

        rbar = np.mean(r)  # center
        xbar = np.mean(x)
        sigma_within = A2[size] * rbar
        sigma_between = self.sigma_between(x, sigma_within, size)

        if hasattr(self, 'calc_method'):
            if self.calc_method == 'standard':
                lcl = xbar - A2[size] * rbar
                ucl = xbar + A2[size] * rbar
            elif self.calc_method == 'extended':
                lcl = xbar - A2[size] * rbar - 1.2 * sigma_between
                ucl = xbar + A2[size] * rbar + 1.2 * sigma_between
        else:
            lcl = xbar - A2[size] * rbar
            ucl = xbar + A2[size] * rbar
        return x, xbar, lcl, ucl, self._title


class Rbar(CCharts):
    _title = "R Chart"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(Rbar, self).__init__()

    def plot(self, data, size):
        if not hasattr(self, 'transform'):
            assert size >= 2
            assert size < 10

        # transform the data if required
        if hasattr(self, 'transform'):
            if self.transform == 'split':
                if hasattr(self, 'split_size'):
                    data = self.split_fix(data, self.split_size)
                else:
                    data = self.split_var(data, size)
            else:
                raise ValueError('No such transformation available')

        r = []  # values
        for xs in data:
            if hasattr(self, 'transform'):
                size = len(xs)
            else:
                assert size == len(xs)
            r.append(max(xs) - min(xs))

        rbar = np.mean(r)  # center

        lcl = D3[size] * rbar
        ucl = D4[size] * rbar

        return r, rbar, lcl, ucl, self._title
