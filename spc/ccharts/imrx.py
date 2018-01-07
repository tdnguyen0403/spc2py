import numpy as np

from .ccharts import CCharts
from .tables import d2


class IMRX(CCharts):
    """ To use for I-MR-R and I-MR-S charts.
    """
    _title = "X Chart"

    def __init__(self, sizecol=1, **kwargs):
        self.kwargs = kwargs
        super(IMRX, self).__init__()
        self.size = sizecol - 1

    def plot(self, data, size):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes

        samples = dict()
        for n, value in zip(sizes, data):
            if n in samples:
                samples[n].append(value)
            else:
                samples[n] = [value]

        sample_size = len(samples[1])
        #        num_samples = len(samples)

        sample_mean = []  # VALUES
        sample_mr = []
        for key in samples:
            assert sample_size == len(samples[key])
            sample_mean.append(np.mean(samples[key]))
            try:
                v1, v2 = sample_mean[-2:]
                sample_mr.append(abs(v1 - v2))
            except:
                sample_mr.append(np.nan)

        xbar = np.mean(sample_mean)
        mrbar = np.nanmean(sample_mr)

        ucl_xbar = xbar + 3 * (mrbar / d2[2])
        lcl_xbar = xbar - 3 * (mrbar / d2[2])

        return sample_mean, xbar, lcl_xbar, ucl_xbar, self._title
