import numpy as np
from scipy.stats import beta, f

from .ccharts import CCharts
from .tables import B3, B4


def cova(mat):
    l, _ = mat.shape
    for i in range(1, l):
        cov = np.hstack((np.array([]), mat.diagonal(i)))
    return cov


def var_cov(var, s):
    varmean = var.mean(axis=0)
    smean = s.mean(axis=0)
    n = len(varmean)
    mat = np.zeros(shape=(n, n)) + np.diag(varmean)

    a, b = 0, n - 1
    for i in range(1, n):
        mat = mat + np.diag(smean[a:b], k=i) + np.diag(smean[a:b], k=-i)
        a, b = b, (b + (b - 1))

    return mat


class TsquareSingle(CCharts):
    _title = "T-square Hotelling Chart"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(TsquareSingle, self).__init__()

    def plot(self, data, size):
        data = np.array(data)
        numsample = len(data)

        colmean = np.mean(data, axis=0)
        matcov = np.cov(data.T)
        matinv = np.linalg.inv(matcov)

        values = []
        for sample in data:
            dif = sample - colmean
            value = matinv.dot(dif.T).dot(dif)
            values.append(value)

        cl = ((numsample - 1) ** 2) / numsample
        lcl = cl * beta.ppf(0.00135, size / 2, (numsample - size - 1) / 2)
        center = cl * beta.ppf(0.5, size / 2, (numsample - size - 1) / 2)
        ucl = cl * beta.ppf(0.99865, size / 2, (numsample - size - 1) / 2)

        return values, center, lcl, ucl, self._title


class Tsquare(CCharts):
    _title = "T-square Hotelling Chart"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(Tsquare, self).__init__()

    def plot(self, data, size):

        sizes = data[:, 0]
        sample = data[:, 1:]

        samples = dict()
        for n, value in zip(sizes, sample):
            if n in samples:
                samples[n] = np.vstack([samples[n], value])
            else:
                samples[n] = value

        m = len(samples.keys())
        n = len(samples[1])
        p = len(samples[1].T)

        variance, S = [], []
        for i in range(m):
            mat = np.cov(samples[i + 1].T, ddof=1)
            variance.append(mat.diagonal())
            S.append(cova(mat))

        variance, S = np.array(variance), np.array(S)

        means = np.array([samples[xs + 1].mean(axis=0) for xs in range(m)])
        means_total = means.mean(axis=0)

        Smat = var_cov(variance, S)
        Smat_inv = np.linalg.inv(Smat)

        values = []
        for i in range(m):
            a = means[i] - means_total
            values.append(5 * a @ Smat_inv @ a.T)

        p1 = (p * (m - 1) * (n - 1))
        p2 = (m * n - m - p + 1)
        lcl = (p1 / p2) * f.ppf(0.00135, p, p2)
        center = (p1 / p2) * f.ppf(0.50, p, p2)
        ucl = (p1 / p2) * f.ppf(0.99865, p, p2)

        return values, center, lcl, ucl, self._title


class Variation(CCharts):
    _title = "Generalized Variance"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        super(Variation, self).__init__()

    def plot(self, data, size):

        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0, ddof=1)
        svalues = []
        for sample in data:
            value = []
            for i in range(size):
                value.append((sample[i] - mean[i]) / std[i])
            a = sum([x * x for x in value])
            b = np.mean(value)
            s = np.sqrt((a - 3 * (b * b)) / 2)
            svalues.append(s)

        sbar = np.mean(svalues)
        lcl = B3[size + 1] * sbar
        ucl = B4[size + 1] * sbar

        return svalues, sbar, lcl, ucl, self._title
