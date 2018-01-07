#!/usr/bin/env python3


from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__version__ = '0.4'
__author__ = "Carlos Silva"
__email__ = "carlosqsilva@outlook.com"

from .ccharts import *
from .spc import SPC
from .rules import Rules

import warnings

warnings.simplefilter("ignore")


