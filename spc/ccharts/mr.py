import numpy as np

from .ccharts import CCharts
from .tables import A2, D3, D4, d2


class MR(CCharts):
    _title = "MR - Moving Range Chart"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(MR, self).__init__()

    def plot(self, data, size):
        assert size == 1

        r = np.array([np.nan] + [abs(data[i] - data[i + 1]) for i in range(len(data) - 1)])

        rbar = np.nanmean(r)

        lclr = D3[2] * rbar
        uclr = D4[2] * rbar

        return r, rbar, lclr, uclr, self._title


class I(CCharts):
    _title = "Individual chart"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(I, self).__init__()

    def plot(self, data, size):
        assert size == 1

        mr = np.array([np.nan] + [abs(data[i] - data[i + 1]) for i in range(len(data) - 1)])

        mrbar = np.nanmean(mr)
        xbar = np.mean(data)
        sigma_within = A2[size] * mrbar
        sigma_between = self.sigma_between(mr, sigma_within, size)

        if hasattr(self, 'calc_method'):
            if self.calc_method == 'standard':
                lcl = xbar - 3 * (mrbar / d2[2])
                ucl = xbar + 3 * (mrbar / d2[2])
            elif self.calc_method == 'extended':
                lcl = xbar - A2[size] * mrbar - 1.2 * sigma_between
                ucl = xbar + A2[size] * mrbar + 1.2 * sigma_between
        else:
            lcl = xbar - 3 * (mrbar / d2[2])
            ucl = xbar + 3 * (mrbar / d2[2])

        return data, xbar, lcl, ucl, self._title
