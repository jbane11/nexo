def search_keywords(text, keywords):
    """
    Searches for a list of keywords in a given text and returns the matched ones.
    
    :param text: The input string to search within.
    :param keywords: A list of keywords to search for.
    :return: A list of matched keywords found in the text.
    """
    found_keywords = [kw for kw in keywords if re.search(rf'\b{re.escape(kw)}\b', text, re.IGNORECASE)]
    return found_keywords

#Function to retrieve run list information
def GetRunInfo(runnumber, old=False):
    global Runlist_DF
    if old:
        print("not set up yet")
        return -1
    
    DF=Runlist_DF.query('`Run No.`== %f'%(runnumber))

    if len(DF)==0:
        print("That run is not in the list")
        return 0
    else:
        return DF
    

def GetBGRun(run):
    global bgdb
    try:
        return bgdb.query("run==%i"%(run)).iloc[0]["background"]
    except:
        return -1


def isAnodeOff(run):
    return  GetRunInfo(run).iloc[0]["Anode V."] == 0 


def find_the_file(RN=596,debug=1):

    ''' find_the_file(Run number)
            This function attempt to find the data file location of of file based on the run number.
           Uses a list of possible locations (locations) to search through. It uses the function 
           GetRunInfo to grab the run information. It needs the date.
    '''
    global locations
    waveformpath=""
    RI = GetRunInfo(RN)
    if type(RI) == type(0) :
        return 0
    RI = RI.iloc[0]
    
    runstr = f"{RN}".zfill(5)

    dir_strs= [f"{RI.Date}-{runstr}",f"{RI.Date}/{RI.Date}-{runstr}"]
    located=0
    for loc in locations:
        for dir_str in dir_strs:
            fullpath= loc + dir_str
            if debug >=10:
                print(fullpath)
            if os.path.exists(fullpath):
                waveformpath=fullpath
                located=1
                if debug >=5 :
                    print("located : ", waveformpath)

    if located == 0:
        return 0
    else :
        return waveformpath

def GetWaveForm(runnumber,wavenumber=11,debug=1):
    global waveform_path
    RI = GetRunInfo(runnumber) 
    RN=runnumber
    if type(RI)==type(0): #Make sure run is in runlist
        return 0
    waveform_date ="%i"%(RI["Date"].iloc[0])
    runnumber="%05i"%(runnumber)
    

    # For left PC
    #waveform_dir=waveform_path+waveform_date+"/"+waveform_date+"-"+runnumber
    waveformpath=find_the_file(RN,debug=debug)
    waveform_dir = waveformpath


    if debug>=10:
        print(waveform_date)
        print(runnumber)
        print(waveform_dir)
        print(waveformpath)

    waveform_wavenumber="%s"%(wavenumber)

    waveform_filename=waveform_date+"-"+runnumber+"_"+"*"+waveform_wavenumber
    waveform_fullpath_wild=waveform_dir+"/"+waveform_filename+".csv"
    try: 
        waveform_fullpath=glob.glob(waveform_fullpath_wild )[-1].replace("\\","/")
    except:
        waveform_fullpath=glob.glob(waveform_dir+"/"+waveform_date+"-"+runnumber+"_"+"*" )[-1].replace("\\","/")
    
    if os.path.exists(waveform_fullpath):
        # Grab the second line and define the units of each column
        with open(waveform_fullpath) as f:
            unit_line=f.readlines()[1]

        if debug>=10:
            print(unit_line)
        units=unit_line.replace("(","").replace(")","").strip().split(",")
        #Build DF from csv
        DF=pd.read_csv(waveform_fullpath,skiprows=[1])
        # Convert to ms and mV
        for i,key in enumerate(DF.keys()):
            if units[i] == "V":
                DF[key]=DF[key]*1000 
            if units[i] == "ms":
                print("time convertion")
                DF[key]=DF[key]*1000 
        # rename columns
        DF=ReNameCols(DF)

        #if checkforshit(DF) == 0:
        #    return DF
        
        
            
        return DF

        
    else: # Did not find file
        print("Issue with file")
        return 0

def GetWaveForm_LaserPower(runnumber,wavenumber=11,debug=1):
    global waveform_path
    RI = GetRunInfo(runnumber) 
    RN=runnumber
    if type(RI)==type(0): #Make sure run is in runlist
        return 0
    waveform_date ="%i"%(RI["Date"].iloc[0])
    runnumber="%05i"%(runnumber)
    

    # For left PC
    #waveform_dir=waveform_path+waveform_date+"/"+waveform_date+"-"+runnumber
    waveformpath=find_the_file(RN,debug=debug)
    waveform_dir = waveformpath


    if debug>=10:
        print(waveform_date)
        print(runnumber)
        print(waveform_dir)
        print(waveformpath)
    if waveform_dir ==0:
        return pd.DataFrame()

    waveform_wavenumber="%s"%(wavenumber)

    waveform_filename=waveform_date+"-"+runnumber+"_"+"*"+waveform_wavenumber
    waveform_fullpath_wild=waveform_dir+"/"+waveform_filename+".csv"
    try: 
        waveform_fullpath=glob.glob(waveform_fullpath_wild )[-1].replace("\\","/")
    except:
        waveform_fullpath=glob.glob(waveform_dir+"/"+waveform_date+"-"+runnumber+"_"+"*" )[-1].replace("\\","/")
    
    if os.path.exists(waveform_fullpath):
        # Grab the second line and define the units of each column
        with open(waveform_fullpath) as f:
            lines = f.readlines()
        unit_line=lines[1]
        
        units=unit_line.replace("(","").replace(")","").strip().split(",")

        #Build DF from csv
        DF=pd.read_csv(waveform_fullpath,skiprows=[1])
        # Convert to ms and mV
        for i,key in enumerate(DF.keys()):
            if units[i] == "V":
                DF[key]=DF[key]*1000 
            if units[i] == "ms":
                print("time convertion")
                DF[key]=DF[key]*1000 
    
    

        #if checkforshit(DF) == 0:
        #    return DF
        
        
            
        return DF

        
    else: # Did not find file
        print("Issue with file")
        return 0


def checkforshit(DF):
    bad=0
    for key in DF.keys():
        if type(DF[key].iloc[1] == type("str")):
            bad =key
        else:
            continue

    return bad
    

# this should correct the colomn names of the avg cath and anode. need to add incorrect options to list
def ReNameCols(DF):
    chann_name_options=[["Avg UV","Avg Anode"],
                        ['Average Cathode (2)', 'Average Anode (2)'],
                        ['average(Cathode)', 'average(Anode)']]
    Correct_names=["Avg Cathode","Avg Anode"]
    keys=DF.keys()
    if Correct_names[0] in keys and Correct_names[1] in keys:
        return DF
    for chan_options in chann_name_options:
        if chan_options[0] in keys:
            DF =DF.rename(columns={chan_options[0]: Correct_names[0]})
        if chan_options[1] in keys:
            DF =DF.rename(columns={chan_options[1]: Correct_names[1]})

    return DF

