import uproot 
import numpy as np
import matplotlib.pyplot as plt
import os,sys,time
import pandas as pd
from pandasgui import show





file="./labview_data/20230609_pid_test_2.txt"
names=["time","xe_cell","cold_fing","nit_res","tc1","tc2","tc3","p_cell","p_man","flow","valv","heat","low_lim","high_lim","res_lim"]
DF=pd.read_table(file,delimiter=",",names=names,skiprows=[0,1,2,3])


show(DF)

