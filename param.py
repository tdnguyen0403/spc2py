import sys, os
import configparser
import pandas as pd
from spc.ccharts import *
from spc.key import FIG_KEY

CONTROL_CHARTS = {"Cusum": [CUSUM],
                  "Ewma": [EWMA],
                  "Xbar_Sbar": [Xbar_Rbar, Sbar],
                  "Xbar_Rbar": [Xbar_Rbar, Rbar],
                  "Individual Moving Range": [I, MR],
                  "C Chart": [C],
                  "NP Chart": [NP],
                  "P Chart": [P],
                  "P' Chart": [PPrime],
                  "U Chart": [U],
                  "U' Chart": [UPrime],
                  "I-MR-R": [IMRX, IMRMR, IMRR],
                  "I-MR-S": [IMRX, IMRMR, IMRStd]}

# set up root folder and import config file
if hasattr(sys, 'frozen'):
    _ROOT = sys._MEIPASS
else:
    _ROOT = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(_ROOT, 'config.ini'))


# define function to check for float
def is_float(string):
    try:
        return float(string)
    except ValueError:  # String is not a number
        return False


# read all control charts classes in config into list of arguments and flatten it
types = config['Type']
charts = []
for chart in types:
    charts.append(CONTROL_CHARTS[types.get(chart, None)])
charts = [item for sublist in charts for item in sublist]

# read all figure argument and combine with FIG_KEY to make dict kwargs
figure = config['Figure']
data = pd.read_csv(os.path.join(_ROOT, 'data\\', figure.get('data', None)))
title = figure.get('title', None)
save_path = figure.get('save_path', _ROOT)
file_name = os.path.join(save_path, title)
fig_arg = dict(zip(FIG_KEY, [title, data, file_name]))

# read each chart args into a list, convert string to float and zip them together with the list of chart classes
try:
    arg_one = config['ChartOne']
    arg_one = {key: float(value) if isinstance(
                                value, str) and is_float(value) else value for key, value in arg_one.items()}
except KeyError:
    arg_one = {}

try:
    arg_two = config['ChartTwo']
    arg_two = {key: float(value) if isinstance(
                                value, str) and is_float(value) else value for key, value in arg_two.items()}
except KeyError:
    arg_two = {}

try:
    arg_three = config['ChartThree']
    arg_three = {key: float(value) if isinstance(
                                value, str) and is_float(value) else value for key, value in arg_three.items()}
except KeyError:
    arg_three = {}

control_charts = dict(zip(charts, [arg_one, arg_two, arg_three]))
