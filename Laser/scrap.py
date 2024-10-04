import numpy as np
import pandas as pd
import matplotlib as plt
from scipy.signal import savgol_filter

data = pd.read_csv("C:\\Users\\mloscar\\Downloads\\laser current v pulse width.csv")
data.head()

# x = 
# y = 
# yhat = savgol_filter(y, 51, 3) # window size 51, polynomial order 3

# plt.plot(x,y)
# plt.plot(x,yhat, color='red')
# plt.show()
