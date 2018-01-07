import numpy as np

from .ccharts import CCharts
from .tables import B3, B4


class IMRStd(CCharts):
    """ To use for I-MR-R and I-MR-S charts.
    """
    _title = "Standard Deviation Chart"

    def __init__(self, sizecol=1, **kwargs):
        self.kwargs = kwargs
        super(IMRStd, self).__init__()
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

        sample_std = []
        for key in samples:
            assert sample_size == len(samples[key])
            sample_std.append(np.std(samples[key], ddof=1))

        sbar = np.mean(sample_std)
        ucl_std = B4[sample_size] * sbar
        lcl_std = B3[sample_size] * sbar

        return sample_std, sbar, lcl_std, ucl_std, self._title
