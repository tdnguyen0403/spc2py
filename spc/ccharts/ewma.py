import numpy as np

from .ccharts import CCharts
from .tables import h4


class EWMA(CCharts):
    _title = "EWMA Chart"

    def __init__(self, target=None, weight=0.2, **kwargs):
        self.kwargs = kwargs
        super(EWMA, self).__init__()
        self.target = target
        self.weight = weight

    def plot(self, data, size):
        assert ((self.weight > 0) and (self.weight < 1))

        if size > 1:
            data = np.mean(data, axis=1)

        target = self.target
        weight = self.weight

        # calculate the target with not given
        if target is None:
            target = np.mean(data)

        # calculate the standard deviation
        rbar = []
        for i in range(len(data) - 1):
            rbar.append(abs(data[i] - data[i + 1]))
        std = np.mean(rbar) / 1.128

        ewma = []  # values
        i = target
        for x in data:
            ewma.append(weight * x + (1 - weight) * i)
            i = ewma[-1]

        lcl, ucl = [], []
        for i in range(1, len(data) + 1):
            lcl.append(target - 3 * std * np.sqrt((weight / (2 - weight)) * (1 - (1 - weight) ** (2 * i))))
            ucl.append(target + 3 * std * np.sqrt((weight / (2 - weight)) * (1 - (1 - weight) ** (2 * i))))

        #        ax.plot([0, len(ewma)], [target, target], 'k-')
        #        ax.plot(lcl, 'r:')
        #        ax.plot(ucl, 'r:')
        #        ax.plot(ewma, 'bo--')

        return ewma, target, lcl, ucl, self._title


class MEWMA(CCharts):
    _title = "MEWMA Chart"

    def __init__(self, lambd=0.1, **kwargs):
        self.kwargs = kwargs
        super(MEWMA, self).__init__()
        self.lambd = lambd

    def plot(self, data, size):

        nrow, ncol = data.shape
        mean = data.mean(axis=0)

        v = np.zeros(shape=(nrow - 1, ncol))
        for i in range(nrow - 1):
            v[i] = data[i + 1] - data[i]

        vv = v.T @ v

        s = np.zeros(shape=(ncol, ncol))
        for i in range(ncol):
            s[i] = (1 / (2 * (nrow - 1))) * (vv[i])

        mx = data - mean

        z = np.zeros(shape=(nrow + 1, ncol))
        for i in range(nrow):
            z[i + 1] = self.lambd * mx[i] + (1 - self.lambd) * z[i]
        z = z[1:, :]

        t2 = []  # values
        for i in range(nrow):
            w = (self.lambd / (2 - self.lambd)) * (1 - (1 - self.lambd) ** (2 * (i + 1)))
            inv = np.linalg.inv(w * s)
            t2.append((z[i].T @ inv) @ z[i])

        ucl = h4[int(self.lambd * 10) - 1][ncol - 1]
        return t2, 0, 0, ucl, self._title
