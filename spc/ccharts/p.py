import numpy as np

from .ccharts import CCharts


class P(CCharts):
    _title = "P Chart"

    def __init__(self, size=1, **kwargs):
        self.kwargs = kwargs
        super(P, self).__init__()
        self.size = size - 1

    def plot(self, data, size):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes

        data2 = data / sizes
        pbar = np.mean(data2)

        for n in sizes:
            assert n * pbar >= 5
            assert n * (1 - pbar) >= 5

        if np.mean(sizes) == sizes[0]:
            size = sizes[0]
            lcl = pbar - 3 * np.sqrt((pbar * (1 - pbar)) / size)
            ucl = pbar + 3 * np.sqrt((pbar * (1 - pbar)) / size)

            if lcl < 0:
                lcl = 0
            if ucl > 1:
                ucl = 1

            return data2, pbar, lcl, ucl, self._title

        else:
            lcl, ucl = [], []
            for size in sizes:
                lcl.append(pbar - 3 * np.sqrt((pbar * (1 - pbar)) / size))
                ucl.append(pbar + 3 * np.sqrt((pbar * (1 - pbar)) / size))

        if hasattr(self, 'ax_format'):
            if self.ax_format == 'ppm':
                data2 = [i * 10 ** 6 for i in data2]
                pbar = pbar * 10 ** 6
                lcl = [i * 10 ** 6 for i in lcl]
                ucl = [i * 10 ** 6 for i in ucl]

        return data2, pbar, lcl, ucl, self._title
