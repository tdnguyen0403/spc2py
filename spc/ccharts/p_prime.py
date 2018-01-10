import numpy as np

from .ccharts import CCharts
from .tables import d2


class PPrime(CCharts):
    _title = "P' Chart"

    def __init__(self, size=1, **kwargs):
        self.kwargs = kwargs
        super(PPrime, self).__init__()
        self.size = size - 1

    def plot(self, data, size):

        sizes, defects = data.T
        data = dict(zip(sizes, defects))

        if self.size == 1:
            sizes, defects = defects, sizes
        # calculate z_score and sigma_p for every data points
        plot_point = defects / sizes
        pbar = np.sum(defects) / np.sum(sizes)
        z_score = []
        for size, defect in data.items():
            pi = defect / size
            sigma_p = np.sqrt((pbar * (1 - pbar)) / size)
            z_score.append((pi - pbar) / sigma_p)

        # estimate variation sigma_z through moving range method for z_score
        r = np.array([np.nan] + [abs(z_score[i] - z_score[i + 1]) for i in range(len(z_score) - 1)])
        mrbar = np.nanmean(r)
        sigma_z = mrbar / d2[2]

        # loop through each subgroup and calculate limits
        lcl, ucl = [], []
        for size in sizes:
            lcl_point = pbar - 3 * np.sqrt((pbar * (1 - pbar)) / size) * sigma_z
            if lcl_point < 0:
                lcl_point = 0
            ucl_point = pbar + 3 * np.sqrt((pbar * (1 - pbar)) / size) * sigma_z
            if ucl_point > 1:
                lcl_point = 1
            lcl.append(lcl_point)
            ucl.append(ucl_point)

        if hasattr(self, 'ax_format'):
            if self.ax_format == 'ppm':
                plot_point = [i * 10 ** 6 for i in plot_point]
                pbar = pbar * 10 ** 6
                lcl = [i * 10 ** 6 for i in lcl]
                ucl = [i * 10 ** 6 for i in ucl]

        return plot_point, pbar, lcl, ucl, self._title
