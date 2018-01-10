#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib as mpl

import numpy as np
import pandas as pd

from .results import PlotCharts
from .key import FIG_KEY

plt.style.use('ggplot')
mpl.rcParams['lines.markersize'] = 5


class SPC(object):
    """
    SPC is the main class of the library. It receive the data, plot the chart
    drop values and save the image to a file.

    :param data: Can be a list, nested list, numpy.array or pandas.Dataframe

    :Example:
    """

    def __init__(self, data=None, **kwargs):

        # convert to numpy array
        if isinstance(data, pd.DataFrame):
            data = data.values

        self.kwargs = kwargs
        for k in self.kwargs.keys():
            if k in FIG_KEY:
                self.__setattr__(k, self.kwargs[k])

        # identify subgroup size
        if isinstance(data[0], (list, tuple, np.ndarray)):
            self.size = len(data[0])
        else:
            self.size = 1

        self.data = data
        self.layers = []
        self.points = None
        self.summary = []

    def __repr__(self):
        self.make()
        self.save(self.file_name)
        plt.show()
        return "<pyspc: (%d)>" % self.__hash__()

    def __getitem__(self, i):
        return self.summary[i]

    def __iter__(self):
        for x in self.summary:
            yield x

    def get_subplots(self):
        if len(self.layers) > 1:
            return self.subplots[0]
        return self.subplots

    def save(self, file_name, **kwargs):
        """
        Save the chart to a image file.

        :param file_name: name of the image file, if no extenssion is provide it will be save as '.png'.
        :param **kwargs: see matplotlib.figure.Figure.savefig for more details.
        """
        self.fig.savefig(file_name, **kwargs)

    def drop(self, *args):
        self.data = np.delete(self.data, args, axis=0)

    def make(self, **kwargs):
        num_layers = len(self.layers)
        if num_layers == 0:
            plt.show()
            return

        self.fig, *self.subplots = plt.subplots(num_layers, **kwargs)

        if hasattr(self, 'title'):
            self.fig.canvas.set_window_title(self.title)
        else:
            self.fig.canvas.set_window_title('SPC Chart')

        for layer, ax in zip(self.layers, self.get_subplots()):
            summary = {}

            values, center, lcl, ucl, title = layer.plot(self.data, self.size)
            PlotCharts(ax, values, center, lcl, ucl, title, **layer.kwargs)

            summary['name'] = title
            summary['values'] = values
            summary['lcl'] = lcl
            summary['ucl'] = ucl
            summary['center'] = center

            if self.points is not None:
                summary['violation-points'] = self.points.plot_violation_points(ax, values, center, lcl, ucl)

        self.fig.tight_layout()
