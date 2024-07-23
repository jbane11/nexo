''' This scipt will attempt to plot the walk on a phase diagram for a thermocpouple
for a a set of time'''


import h5py, os ,sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob,os,platform
import datetime,calendar


#varible for determining the lab pc or other pc, Check if windows or not, then try to grab pc name
pcname=""
if platform.system() == "Windows":
    pcname=platform.uname().node
else:
    try:
        pcname=os.uname()[1]
    except:
        print("Issue with finding pc name")

env_var_dataloc ="" #varible for location of waveform data. 
data_dir_mod_old="" #varible for small difference in storage managment between pc 1 and 2
if pcname=='PHYS-PSB02802': #Lab pc 2, (Labview pc)
    env_var_dataloc ="A:/DATA/"
    
elif pcname=="PHYS-PSB02801": #Lab pc 1, (solidworks pc)
    env_var_dataloc ="data/" #This is true for Jason's work atm (June 10th) Needs Updateing to global or user friendly verison
    data_dir_mod_old="/"


TimeZero=datetime.datetime(2023,1,1)


groups = []
datasets = []
atts = {} # attributes

def GetPhaseDiagram():
    ''' Function to get the phase diagram info for xenon.
    returns two arrays pressures and temps for phase lines '''
    
    pfilename="A/Labview20/slow control/plot/xpd/pressures.txt"
    tfilename="A/Labview20/slow control/plot/xpd/temps.txt"
    P = open(pfilename).readlines()
    T = open(tfilename).readlines()
    return P,T


def gather_names_and_atts(name, obj):
    if isinstance(obj, h5py.Group):
        groups.append(name)
    elif isinstance(obj, h5py.Dataset):
        datasets.append(name)
    for key, val in obj.attrs.items():
        atts[name + '/' + key] = val

def list_groups_datasets_atts(file):
    with h5py.File(file, 'r') as f:
        f.visititems(gather_names_and_atts)

def print_lists(list_name):
    i = 0
    for name in list_name:
        print(i, name)
        i=i+1
    print()

def create_dataframe_from_datasets(file_name, dataset_names):

    with h5py.File(file_name, 'r') as f:
        dataset_names =[]
       
        for i in f.keys():
            for j in f[i].keys():
                dataset_names.append(i+"/"+j)
       
        
        dfs = {name: pd.DataFrame(f[name][:])   for name in dataset_names }
    return dfs


def poop():
    with h5py.File(file_name, 'r') as f:
        for name in dataset_names:
            try:
                dfs = {name: pd.DataFrame(f[name][:]) }
            except:
                print("issue with", name)
    return dfs

channel_list=  ["Flow_Meter" ,"Liquid_Nitro_Valve", "PID_Heater","Pressure_1","Pressure_2",
                "Heater_State","Nitro_Baseline","Nitro_Weigth","Target_Channel","Target_Temperature",
                "Time","Valve_State","Cold_Finger","Nitro_Reservoir","Xe_Cell_1","Xe_Cell_2",
                "Xe_Cell_3","Xe_Cell_Outside","Pressure_Cell","Pressure_Mfold","Storage_1","Storage_2",
                "Pressure_Cryostat","Pressure_Manifold","Pressure_Nitro","Cryostat_Top","Xe_Cell_Bottom","Xe_Cell_Top"]


def getprologue_time(f):
    ''' Argument f == hdf5 file
        returns datetimeobject of time information 
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
    
    strtime=""
    for key in timeinfo.keys():
        strtime=strtime+"%s"%(str(timeinfo[key]))
    RunStart_Datetime=datetime.datetime.strptime(strtime, "%Y%m%d%H%M%S") #takes a string in the listed format and turns it into a datetime object


    print(timeinfo, RunStart_Datetime)
    return RunStart_Datetime 

def timetosecs(timeinfo):
    '''argument timeinfo dict returns total seconds for the day
    Need to make this return time from some time in the past to allow for overnight runs'''


    return timeinfo["hour"]*60*60 +timeinfo["min"]*60+timeinfo["sec"]



def calib_dict_wtime(file_name):
    ''' This function grabs the slow control data from the hdf5 file that offsets the time by amount of seconds since Jan 1 2020'''
    fh5= h5py.File(file_name, 'r') 
    timeinfo=getprologue_time(fh5)
    timeoffset=(timeinfo-TimeZero).total_seconds()
    print("Time offset",timeoffset)
    fh5.close()
    list_groups_datasets_atts(file_name)
    dataset_names = datasets # to create a dataframe for each
    datadict = create_dataframe_from_datasets(file_name, dataset_names)
    newdict={}
    l,m,n=-1,-1,-1
    j=0
    js=[-1,-1,-1]
    print(datadict.keys())
    for key in datadict.keys():

        #print(key)
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

        if s_key =="Pressure_1":
            s_key="Pressure_Cell"
        elif s_key =="Pressure_2":
            s_key="Pressure_Manifold"
        if s_key not in channel_list:
            
           print("Not in channel list " ,s_key)
           # continue

        if s_key=="Inter" or s_key =="Slope":
                continue
        
        else:
            
            #print(group,key, js[j])
            if j==1:
                m,b=1,0
            else:
                try:
                    m = datadict["%s/Slope"%(group)][0][js[j]]
                    b = datadict["%s/Inter"%(group)][0][js[j]]
                except:
                    m,b=1,0
        
            
        #print(m,b, )
        
        newdict[s_key]=datadict[key][0]*m +b
    
    try:
        newdict["Time"] = timeoffset + np.arange(0,len(newdict["Time"])*2,2)
    except:
        newdict["Time"] = timeoffset + np.arange(0,len(newdict[s_key])*2,2)
    
    return newdict



def get_slow_ctr_df(filedate):

    filedes ="slow_control"
    datadir="./data"
    
    try:
        filedate=str(filedate)
    except:
        print("Issue with file date")

    filelist=glob.glob("%s/%s*.h5"%(datadir,filedate))
    print(filelist)
    if len(filelist) <1:
        print("Error with globing files")

    datadicts=[]
    DFs=[]
    for filename in filelist:
      
        finfo=os.stat(filename)
        print(finfo.st_size)
        if finfo.st_size < 18000:
            print("Skipping %s due to size"%(filename))
            continue
        datasets = []
        print(filename)
        datadict=calib_dict_wtime(filename)
        datadicts.append(datadict)
        try:
            DFs.append(pd.DataFrame.from_dict(datadict))
        except:
            print("issue with appending files into list")
        print( "len",len(datadict["Time"]))

    DF = pd.concat(DFs)
    DF =DF.sort_values(by=["Time"])

    return DF




def fixtimeoffset(DFs): 
    '''This function will take a list of '''

def GetAllFiles(date):
    if type(date)==type("str") or type(date) == type(2):
        date_placeholder=date
        date=[]
        date.append(date_placeholder)
    elif type(date) != type(["str","str"]):
        print("Issue with argument - date \n Please use string or list of strings in the format YYYYMMDD")
        return [""]
    file_list=[]
    for d in date:
        search_term=env_var_dataloc+str(d)+"*"
        file_list=file_list+glob.glob(search_term)
    return file_list


def Get_SlowControl_DF_fromlist(filelist):
    if type(filelist)==type("str"):
        filelist_placeholder=filelist
        filelist=[]
        filelist.append(date_placeholder)
    elif type(file_list) != type(["str","str"]):
        print("Issue with argument - date \n Please use string with the filepath")
        return [""]
    slowcontrol_dict_list=[]
    for file in file_list:
        if os.path.getsize(file) <=30000:
            continue
        slowcontrol_dict_list.append(pd.DataFrame.from_dict(calib_dict_wtime(file)))
        DF=pd.concat(slowcontrol_dict_list)
    return DF

def Get_SlowControl_DF(date):
    DF=pd.DataFrame()
    if type(date)==type("str") or type(date) == type(2):
        date_placeholder=date
        date=[]
        date.append(date_placeholder)
    elif type(date) != type(["str","str"]):
        print("Issue with argument - date \n Please use string or list of strings in the format YYYYMMDD")
        return DF
    file_list=GetAllFiles(date)
    slowcontrol_dict_list=[]
    for file in file_list:
        if os.path.getsize(file) <=30000:
            print("Skipping %s"%(file))
            continue
        slowcontrol_dict_list.append(pd.DataFrame.from_dict(calib_dict_wtime(file)))
        DF=pd.concat(slowcontrol_dict_list)
    return DF



''' The starting arguments will be channel name and  time start and end'''

argv = sys.argv
channel=""
time_start_index=0
time_stop_index=-1

print(len(argv), argv)

try :
    filedate=argv[1]
except:
    print("Issue with filename, Please run again with  fillname including path")
    exit()


if  len(argv) > 2:
    channel = argv[2]
else :
    channel="Xe_Cell_Bottom"
    time_start_index=0
    time_stop_index=-1
if len(argv) > 3:
    time_start_index = int(argv[3])
else:
    time_start_index=0
    time_stop_index=-1
if len(argv) > 4:
    time_stop_index = int(argv[4])
else:
    time_stop_index=-1


print("Channel ", channel)
print("index for starting ", time_start_index)
print("index for stoping ",  time_stop_index)

print(" File exsits :", os.path.exists(filedate))

DF=Get_SlowControl_DF(filedate)
print(len(DF["Time"]))
print(DF["Time"].iloc[int(time_start_index)],DF["Time"].iloc[int(time_stop_index)])
DF=DF[int(time_start_index):int(time_stop_index)]
#fig2,bx = plt.subplots()
fig,ax = plt.subplots()

Phaswalk=ax.scatter(x=DF[channel],y=DF["Pressure_Cryostat"],c=DF["Time"]-DF["Time"].iloc[0])
ax.set_xlabel("Temp [k]")
ax.set_ylabel("Pressure [psia]")

P,T = GetPhaseDiagram()
ax.scatter(x=T, y=P, c="red")

max=max(DF[channel])+2
min=min(DF[channel])-2
ax.set_xlim(min,max)
fig.colorbar(Phaswalk)

ax.grid()
plt.show()

#bx.errorbar(x=DF["Time"],y=DF["Flow_Meter"])
#bx.grid()
#plt.show()

