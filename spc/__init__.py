#!/usr/bin/env python3


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__version__ = '0.1'
__author__ = "Nguyen Tuan Dat"
__email__ = "nguyentuandat0403@gmail.com"

from .ccharts import *
from .spc import SPC
from .rules import Rules

import warnings

warnings.simplefilter("ignore")


