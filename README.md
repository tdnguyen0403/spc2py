# spc2py

Statistical Process Control Charts Library

spc2py is a Python library aimed to make Statistical Process Control Charts as easy as possible.

It heavily wraps around pyspc with added features


## Features

Control Charts by Variables
* Mean and Range (with Extended limit calculation)
* Mean and Standard Deviation (with Extended limit calculation)
* Individual Values and Moving Range
* Individual values with subgroups
* Exponentially Weighted Moving Average (EWMA)
* Cumulative Sum (CUSUM)

Control Charts by Attributes
* P Chart
* P' Chart (Laney P Chart)
* NP Chart
* C Chart
* U Chart
* U' Chart (Laney U Chart)


Configuration files (config.ini)
* All chart setting can be setup in config.ini
* It will be automatically load when call spc2py.py
* 3 main sections (Chart Type, Figure Setting, Chart Setting)

##Installation
```bash
$ pip install spc2py
```

## Usage
```python
from param import *
from spc import *

p = SPC(**fig_arg) + Rules()
for chart, kwargs in control_charts.items():
    p += chart(**kwargs)
print(p)
```

it comes with 18 sample datasets to play with, available in **./spc2py/data**, you can use your own data (of course). Your data can be nested lists, numpy array or pandas DataFrame.

