#!/usr/bin/env python3

import numpy as np
import matplotlib.ticker as mtick
from .key import ax_key_list

class PlotCharts(object):
    """Use to plot overall format of the chart including axes, plot value,
    center value, ucl, lcl and title. Scaling / adjusting is also included
    """

    def __init__(self, ax, values, center, lcl, ucl, title, **kwargs):
        for k in kwargs.keys():
            if k in ax_key_list:
            # if k in ax_key_list.keys() and type(self) in ax_key_list[k]:
                self.__setattr__(k, kwargs[k])
        self.plot_chart(ax, values, center, lcl, ucl, title)

    def plot_chart(self, ax, values, center, lcl, ucl, title):
        """
        """
        ax.yaxis.tick_right()
        if hasattr(self, 'ax_format'):
            if self.ax_format == 'percent':
                ax.yaxis.set_major_formatter(
                    mtick.PercentFormatter(xmax=1.0, decimals=2))
            elif self.ax_format == 'ppm':
                ax.yaxis.set_major_formatter(
                    mtick.FormatStrFormatter('%.0f' + ' ' + 'ppm'))
        else:
            ax.yaxis.set_major_formatter(
                mtick.FormatStrFormatter('%.3f'))

        if isinstance(values[0], list):
            num = len(values[0])
        else:
            num = len(values)

        newx = list(range(num))
        # fill up space on both side of the chart
        newx[0] = -0.3
        newx[-1] = num - 0.6

        if isinstance(lcl, list) and isinstance(ucl, list):
            ax.yaxis.set_ticks([center])
            ax.plot([-0.3, num], [center, center], 'b--')
            ax.plot(values, 'bs-')
            ax.fill_between(newx, lcl, ucl, color='#009966',
                            alpha=0.3, step='mid')
            ax.step(newx, lcl, 'b-', where='mid')
            ax.step(newx, ucl, 'b-', where='mid')
        else:
            ax.yaxis.set_ticks([lcl, center, ucl])
            ax.plot([0, num], [center, center], 'b--')
            ax.plot([0, num], [lcl, lcl], 'b-')
            ax.plot([0, num], [ucl, ucl], 'b-')
            ax.fill_between([-0.3, num], [lcl, lcl], [ucl, ucl], color='#009966',
                            alpha=0.3)
            # only for CUSUM chart
            if isinstance(values[0], list):
                ax.plot(values[0], 'bs-')
                ax.plot(values[1], 'bs-')
            else:
                ax.plot(values, 'bs-')
        if hasattr(self, 'usl'):
            ax.plot([0, num], [self.usl, self.usl], 'r-')
        if hasattr(self, 'lsl'):
            ax.plot([0, num], [self.lsl, self.lsl], 'r-')

        # Set the title
        ax.set_title(title)

        # Change the y limits of the graph
        ylim = ax.get_ylim()
        factor = 0.2
        new_ylim = (ylim[0] + ylim[1]) / 2 + np.array((-0.5, 0.5)) * (ylim[1] - ylim[0]) * (1 + factor)
        if lcl == 0:
            ax.set_ylim([0, new_ylim[1]])
        else:
            ax.set_ylim(new_ylim)

        # Change x ticks
        new_xlim = [0, num]
        ax.set_xlim([0, num] + np.array((-0.3, -0.6)))
        ax.xaxis.set_ticks(np.arange(*new_xlim, np.ceil(num / 20)))
