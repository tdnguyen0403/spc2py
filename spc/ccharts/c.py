import numpy as np

from .ccharts import CCharts


class C(CCharts):
    _title = "C chart"

    def __init__(self, size=1, **kwargs):
        self.kwargs = kwargs
        super(C, self).__init__()
        self.size = size - 1

    def plot(self, data, size):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes

        # the samples must have the same size for this charts
        assert np.mean(sizes) == sizes[0]

        cbar = np.mean(data)

        lcl = cbar - 3 * np.sqrt(cbar)
        ucl = cbar + 3 * np.sqrt(cbar)

        if hasattr(self, 'ax_format'):
            if self.ax_format == 'ppm':
                data = [i * 10 ** 6 for i in data]
                cbar = cbar * 10 ** 6
                lcl = lcl * 10 ** 6
                ucl = ucl * 10 ** 6

        #        ax.plot([0, len(data)], [cbar, cbar], 'k-')
        #        ax.plot([0, len(data)], [lcl, lcl], 'r:')
        #        ax.plot([0, len(data)], [ucl, ucl], 'r:')
        #        ax.plot(data, 'bo-')

        return data, cbar, lcl, ucl, self._title
