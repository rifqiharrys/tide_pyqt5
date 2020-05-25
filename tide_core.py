#!/usr/bin/python3

from tdr_py.vp_tide import v_input, v_merge, v_dirmerge
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from ttide import t_tide
from utide import solve, reconstruct

'''
arg input
#1 = python file
#2 = file path


'''
arginput = sys.argv
filePath = Path(arginput[1])
raw = pd.read_csv(filePath, sep='\t', index_col='Time')
raw.index = pd.to_datetime(raw.index, dayfirst=True)

