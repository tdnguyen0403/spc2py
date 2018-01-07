import numpy as np

from .ccharts import CCharts


class U(CCharts):
    _title = "U Chart"

    def __init__(self, size=1, **kwargs):
        self.kwargs = kwargs
        super(U, self).__init__()
        self.size = size - 1

    def plot(self, data, size):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes
            print('oi')

        data2 = data / sizes
        ubar = np.sum(data) / np.sum(sizes)

        lcl, ucl = [], []
        for size in sizes:
            lcl.append(ubar - 3 * np.sqrt(ubar / size))
            ucl.append(ubar + 3 * np.sqrt(ubar / size))

        if hasattr(self, 'ax_format'):
            if self.ax_format == 'ppm':
                data2 = [i * 10 ** 6 for i in data2]
                ubar = ubar * 10 ** 6
                lcl = [i * 10 ** 6 for i in lcl]
                ucl = [i * 10 ** 6 for i in ucl]

        return data2, ubar, lcl, ucl, self._title
