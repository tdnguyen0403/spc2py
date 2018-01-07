import numpy

from .ccharts import CCharts


class NP(CCharts):
    _title = "NP Chart"

    def __init__(self, size=1, **kwargs):
        self.kwargs = kwargs
        super(NP, self).__init__()
        self.size = size - 1

    def plot(self, data, size):

        sizes, data = data.T
        if self.size == 1:
            sizes, data = data, sizes

        # the samples must have the same size for this charts
        assert numpy.mean(sizes) == sizes[0]

        p = numpy.mean([float(d) / sizes[0] for d in data])
        pbar = numpy.mean(data)

        lcl = pbar - 3 * numpy.sqrt(pbar * (1 - p))
        ucl = pbar + 3 * numpy.sqrt(pbar * (1 - p))

        if hasattr(self, 'ax_format'):
            if self.ax_format == 'ppm':
                data = [i * 10 ** 6 for i in data]
                pbar = pbar * 10 ** 6
                lcl = lcl * 10 ** 6
                ucl = ucl * 10 ** 6
        #
        return data, pbar, lcl, ucl, self._title
