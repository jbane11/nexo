### This is a header file for useful functions for waveform analysis for Lab 28s drift cell. 
#Import needed libraries
import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import csv
import datetime
import os,platform
from scipy.optimize import curve_fit
import scipy
from scipy.fft import fft, rfft, irfft,ifft,fftfreq
from scipy.signal import argrelextrema
from scipy.stats import norm
from lmfit.models import SkewedGaussianModel


#The path structure I am trying to get working will try to use NAS drive the path for all files

#Path of the NAS drive. This will need to be updated per computer"
NasDrive_path = r"\\172.24.54.234/NAS-Lab28/"

#DataBase filenames
Runlist_filename        = NasDrive_path+ "Databases/Runlist.csv"
AnodeOfflist_filename   = NasDrive_path+ "Databases/bg_db.csv" 
CellDistance_DB_filename= NasDrive_path+ "Databases/CellDistanceDataBase.csv"

#Check if the runlist exits, exit if it doesnt!
if not os.path.exists(Runlist_filename):
    print("Issue with Runlist")
    print(f"{Runlist_filename} does not exist")
    exit

#Read in the runlist and setup column names and value type
Runlist_DF = pd.read_csv(Runlist_filename,index_col=False)
Runlist_DF["RN"]=Runlist_DF["Run No."]
number_cols=["Anode V.","Anode Grid V.","Cathode V.","Cathode Grid V.","Drift Length"]
Runlist_DF[number_cols] = Runlist_DF[number_cols].apply(pd.to_numeric)

#Read in cell distance db and add drift distance, and preamp cal to runlist
Distance_Database=pd.DataFrame()
try: 
    Distance_Database=pd.read_csv(CellDistance_DB_filename)
except:
    print("Issue with drift distance and calibration database")
Distance_Database["Date"] = Distance_Database["Date"].astype(str)
Distance_Database["Date"] = pd.to_datetime(Distance_Database["Date"])

# Add in distance to run list and calc fields
skip=0
for i,run in enumerate(Runlist_DF["Run No."][skip:]):
    Date = pd.to_datetime(Runlist_DF["Date"].iloc[i+skip],format='%Y%m%d')
    DF =Distance_Database[Distance_Database["Date"]<= Date].iloc[0]
    for key in DF.keys()[1:]: 
        Runlist_DF.loc[i+skip,key] = DF[key]



Runlist_DF["Drift Field"] = (Runlist_DF["Cathode Grid V."] - Runlist_DF["Anode Grid V."])/(Runlist_DF["Drift Length"]/10.0)
Runlist_DF["Extraction Field"] = (Runlist_DF["Cathode V."] - Runlist_DF["Cathode Grid V."])/(Runlist_DF["Extraction Distance"]/10.0)
Runlist_DF["Collection Field"] = (Runlist_DF["Anode V."] - Runlist_DF["Anode Grid V."])/(Runlist_DF["Collection Distance"]/10.0)
Runlist_DF["Drift Distance"] = Runlist_DF["Drift Length"] + Runlist_DF["Extraction Distance"] + Runlist_DF["Collection Distance"]
Runlist_DF["Drift Distance Error"] = np.sqrt(Runlist_DF["Drift Length Error"]**2 + Runlist_DF["Collection Distance Error"]**2 + Runlist_DF["Extraction Distance Error"]**2)


print(Runlist_DF.head())












