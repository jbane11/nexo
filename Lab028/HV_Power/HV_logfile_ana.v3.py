
#Imports
import matplotlib.pyplot as plt
import os,sys,argparse,time,math,time
import numpy as np

import pandas as pd
parameter_list=["VMon","IMonL","IMonH","VSet","ISet","ChStatus"]

last_parameter=""
last_time=""
last_chan=""


#debug=5
class Event:
    def __init__(self, timestamp: time.struct_time, parameter: str, value: any):
        self.timestamp = timestamp
        self.parameter = parameter
        self.value = value

    def add_event(self, parameter: str, value: any):
        self.parameter = parameter
        self.value = value

class Channel:
    def __init__(self, Name: any):
        self.name=Name
        self.parameters = {}  # Dictionary to store parameter names and their associated arrays

    def add_parameter(self, parameter_name: str, values: list):
        """Adds a parameter and its associated values array to the channel."""
        self.parameters[parameter_name] = values

    def get_parameter(self, parameter_name: str):
        """Retrieves the values array associated with a parameter name."""
        return self.parameters.get(parameter_name, None)

    def append_to_parameter(self, parameter_name: str, new_values: list):
        """Appends new values to an existing parameter's array. 
        If the parameter does not exist, it creates a new one."""
        if parameter_name in self.parameters:
            self.parameters[parameter_name].extend(new_values)
        else:
            self.add_parameter(parameter_name, new_values)

    def __str__(self):
        return f"Channel with parameters: {self.parameters}"





def argumentparse(argv):
    # Create the parser
    parser = argparse.ArgumentParser(description="A simple example of argparse")

    # Add arguments CAENGECO2020.log
    parser.add_argument("--logfilename", type=str, help="Name of the log file",default="CAENGECO2020.log")
    parser.add_argument("--logfilebase", type=str, help="Display the square of the number",default="/Users/jasonbane/Documents/")
    parser.add_argument("--cont", action="store_true", help="Do you want the script to continue to update")
    parser.add_argument("--debug",type=int,help="Set the level of print debugging 0-10, 10=most",default=1)
    parser.add_argument("--startdate",type=str,help="Date to start graphs in the from of yyyymmdd",default=-1)
    parser.add_argument("--starttime",type=str,help="Time to start graphs in the from of hhmm",default=-1)
    

    # Parse the arguments
    args = parser.parse_args()
    return args


def openlogfile(Args):
    logfile_path=Args.logfilebase+Args.logfilename
    debug=Args.debug
    if os.path.exists(logfile_path):
        return open(logfile_path)
    else:
        print("\n\n\tIssue with finding logfile")
        print(logfile_path, ":: does not exist.")
        print(Args.logfilebase, ":: Double check the base dictory location for logfile.")
        print(Args.logfilename, ":: Double check the name given for the log file.")
        print("\t\tExiting\n\n\n")
        exit()

def closelogfile(logfile):
    close(logfile)
    return


def check_newevent(timestamp):
    print("Not Ready")

def typeofevent(timestamp,par,chan):
    #pull the global varibles for c parameter and time
    global last_parameter
    global last_time
    global last_chan
    event_type=""
    if timestamp==last_time:
        "This is new event"
        event_type="repeat"
        if par==last_parameter and chan == last_chan:
            event_type="repeat par"
            last_chan=chan 
        last_chan=chan   

    else:
        event_type="new"
        last_parameter=par
        last_time=timestamp
        last_chan=chan

    return event_type
    
   

def first_readfile(Args):
    infile=openlogfile(Args)
    debug=Args.debug
    freshstep=0
    
    Event_list=[]
    Channel_list=[Channel(0),Channel(1),Channel(2),Channel(3)]
    

    #Build up channels and parameters
    for channel in Channel_list:
        for parameter in parameter_list:
            channel.add_parameter(parameter,[(0,"0.0000")])

    #Number of unique time stamps
    event_count=1



    for line in infile.readlines()[::1]:


        line_elements=line.split(" ")

        raw_timestamp=line_elements[0].replace("[","").replace("]","").replace("T"," ")
        # Convert the string to a struct_time object
        struct_time = time.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S:")
        # Convert the struct_time object to a timestamp (seconds since the epoch)
        timestamp = time.mktime(struct_time)
    
        #Grab channel, parameter and value
        #print(line_elements)
        ch=line_elements[5][1:-1]
        par=line_elements[7][1:-1]
        val=line_elements[9][1:-2]


        
        eventtype=typeofevent(timestamp,par,ch)
        if debug > 4: print(timestamp,raw_timestamp,ch,par,val,eventtype)

        Channel_list[int(ch)].append_to_parameter(par,[(timestamp,val)])

    return Channel_list


def main(Args):
    ''' Main script for doing work'''
    debug=Args.debug


def read_newdata(Args):
    file =openlogfile(Args)
    debug=Args.debug
    Channel_list_new=[Channel(0),Channel(1),Channel(2),Channel(3)]
    

    #Build up channels and parameters
    for channel in Channel_list_new:
        for parameter in parameter_list:
            channel.add_parameter(parameter,[(0,"0.0000")])

    for line in file.readlines()[-10:]:
        line_elements=line.split(" ")

        raw_timestamp=line_elements[0].replace("[","").replace("]","").replace("T"," ")
        # Convert the string to a struct_time object
        struct_time = time.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S:")
        # Convert the struct_time object to a timestamp (seconds since the epoch)
        timestamp = time.mktime(struct_time)
    
        #Grab channel, parameter and value
        #print(line_elements)
        ch=line_elements[5][1:-1]
        par=line_elements[7][1:-1]
        val=line_elements[9][1:-2]

        eventtype=typeofevent(timestamp,par,ch)
        if debug > 4: print(timestamp,raw_timestamp,ch,par,val,eventtype)

        Channel_list_new[int(ch)].append_to_parameter(par,[(timestamp,val)])
    
    return Channel_list_new

if __name__ == "__main__":
    Args=argumentparse(sys.argv[1:])
    print(Args)

    Channel_list=first_readfile(Args)
    data_array=np.array(Channel_list[0].get_parameter("VMon"))
    x=data_array[1:,0].astype(float)
    y=data_array[1:,1].astype(float)
    x=x-x[0]

    # plt.ion()
    # fig, ax = plt.subplots()
    # line, = ax.errorbar([], [], 'b-o')  # Blue line with circle markers

    i =0
    while True:
        print(i,time.ctime())
        new_Channel_list=read_newdata(Args)



        # line.set_xdata(xdata)
        # line.set_ydata(ydata)

        # ax.relim()
        # ax.autoscale_view()

        # plt.draw()
        time.sleep(2)

        
       
        if i >=100:
            break
        i=i+1
    











    





