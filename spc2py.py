#!/usr/bin/env python3

from param import *
from spc import *

if __name__ == '__main__':

    p = SPC(**fig_arg) + Rules()
    for chart, kwargs in control_charts.items():
        p += chart(**kwargs)
    print(p)
