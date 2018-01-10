#!/usr/bin/env python3

import numpy as np

from ..key import AX_KEY
from .tables import d2
from ..spc import SPC


class CCharts(object):

    def __init__(self):
        self.layers = [self]
        for k in self.kwargs.keys():
            if k in AX_KEY:
                self.__setattr__(k, self.kwargs[k])

    def __radd__(self, model):
        if isinstance(model, SPC):
            model.layers += self.layers
            return model

    def sigma_between(self, data, sigma_within, size):
        mr = np.array([np.nan] + [abs(data[i] - data[i + 1]) for i in range(len(data) - 1)])
        mrbar = np.nanmean(mr)
        sigma_between = np.max([0, (np.sqrt((mrbar / d2[2]) * 2 - (sigma_within * 2 / size)))])
        return sigma_between

    def split_fix(self, data, split_size):
        if len(data[0]) >= 2:
            data = np.squeeze(data.T[1])
        else:
            data = np.squeeze(data.T[0])

        if (len(data) % split_size) != 0:
            start_index = len(data) % split_size
            data = data[start_index:]

        data = np.split(data, len(data) // split_size)
        data = np.vstack(data)
        return data

    def split_var(self, data, size):
        sizes, data = data.T
        if size == 1:
            sizes, data = data, sizes

        samples = dict()
        for n, value in zip(sizes, data):
            if n in samples:
                samples[n].append(value)
            else:
                samples[n] = [value]
        samples = list(samples.values())
        return np.array(samples)
