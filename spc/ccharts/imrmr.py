import numpy as np

from .ccharts import CCharts
from .tables import D3, D4


class IMRMR(CCharts):
    """ To use for I-MR-R and I-MR-S charts.
    """
    _title = "Moving Range Chart"

    def __init__(self, sizecol=1, **kwargs):
        self.kwargs = kwargs
        super(IMRMR, self).__init__()
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

        sample_mr = []
        sample_mean = []
        for key in samples:
            assert sample_size == len(samples[key])
            sample_mean.append(np.mean(samples[key]))
            try:
                v1, v2 = sample_mean[-2:]
                sample_mr.append(abs(v1 - v2))
            except:
                sample_mr.append(np.nan)

        mrbar = np.nanmean(sample_mr)  # CENTER
        ucl_mr = D4[2] * mrbar
        lcl_mr = D3[2] * mrbar

        #        ax.plot([0, num_samples], [mrbar, mrbar], 'k-')
        #        ax.plot([0, num_samples], [lcl_mr, lcl_mr], 'r:')
        #        ax.plot([0, num_samples], [ucl_mr, ucl_mr], 'r:')
        #        ax.plot(sample_mr, 'bo--')

        return sample_mr, mrbar, lcl_mr, ucl_mr, self._title
