
import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

def getprologue_time(f):
    ''' Argument f == hdf5 file
        returns dict of time information 
    '''
    atr="Prologue"
    prologue=f.attrs[atr]
    prologue=prologue.replace("\r","")
    splitlog=prologue.split( "\n")
    timeinfostr=splitlog[2]
    timeinfo={}
    timeinfo["year"]=int(timeinfostr[0:4])
    timeinfo["mon"]=int(timeinfostr[4:6])
    timeinfo["day"]=int(timeinfostr[6:8])
    timeinfo["hour"]=int(timeinfostr[8:10])
    timeinfo["min"]=int(timeinfostr[10:12])
    timeinfo["sec"]=int(timeinfostr[12:14])
    return timeinfo

def timetosecs(timeinfo):
    '''argument timeinfo dict 
    returns total seconds '''
    return timeinfo["hour"]*60*60 +timeinfo["min"]*60+timeinfo["sec"]



def calib_dict_wtime(file_name):


    fh5= h5py.File(file_name, 'r') 

    timeinfo=getprologue_time(fh5)
    timeoffset=timetosecs(timeinfo)
    fh5.close()
    list_groups_datasets_atts(file_name)


    dataset_names = datasets # to create a dataframe for each
    datadict = create_dataframe_from_datasets(file_name, dataset_names)
    newdict={}
    l,m,n=-1,-1,-1
    j=0
    js=[-1,-1,-1]
    for key in datadict.keys():
        pos=key.find("/")
        group=key[:pos]
        
        if group=="omb_daq":
            j=0
            l+=1
            js[0]+=1
        elif group=="pid_info":
            j=1
            m+=1
            js[1]+=1
        elif group=="tc08_daq":
            j=2
            n+=1
            js[2]+=1
        
        m,b=1,0
        s_key=key[pos+1:]

        if s_key=="Inter" or s_key =="Slope":
                continue
        
        else:
            
            print(group,key, js[j])
            if j==1:
                m,b=1,0
            else:
                m = datadict["%s/Slope"%(group)][0][js[j]]
                b = datadict["%s/Inter"%(group)][0][js[j]]
        
            
        print(m,b, )
        
        newdict[s_key]=datadict[key][0]*m +b

    newdict["Time"] = timeoffset + np.arange(0,len(newdict["Time"]))*2


    return newdict
