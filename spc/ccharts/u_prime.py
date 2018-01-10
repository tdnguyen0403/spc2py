import numpy as np

from .ccharts import CCharts
from .tables import d2


class UPrime(CCharts):
    _title = "U' Chart"

    def __init__(self, size=1, **kwargs):
        self.kwargs = kwargs
        super(UPrime, self).__init__()
        self.size = size - 1

    def plot(self, data, size):

        sizes, defects = data.T
        data = dict(zip(sizes, defects))

        if self.size == 1:
            sizes, defects = defects, sizes

        # calculate z_score and sigma_u for every data points
        plot_data = defects / sizes
        ubar = np.sum(defects) / np.sum(sizes)
        z_score = []
        for size, defect in data.items():
            ui = defect / size
            sigma_u = np.sqrt(ubar / size)
            z_score.append((ui - ubar) / sigma_u)
        # estimate variation sigma_z through moving range method for z_score
        r = np.array([np.nan] + [abs(z_score[i] - z_score[i + 1]) for i in range(len(z_score) - 1)])
        mrbar = np.nanmean(r)
        sigma_z = mrbar / d2[2]

        # loop through each subgroup and calculate limits
        lcl, ucl = [], []
        for size in sizes:
            lcl_point = ubar - 3 * np.sqrt(ubar / size) * sigma_z
            if lcl_point < 0:
                lcl_point = 0
            ucl_point = ubar + 3 * np.sqrt(ubar / size) * sigma_z
            lcl.append(lcl_point)
            ucl.append(ucl_point)

        if hasattr(self, 'ax_format'):
            if self.ax_format == 'ppm':
                plot_data = [i * 10 ** 6 for i in plot_data]
                ubar = ubar * 10 ** 6
                lcl = [i * 10 ** 6 for i in lcl]
                ucl = [i * 10 ** 6 for i in ucl]

        return plot_data, ubar, lcl, ucl, self._title
