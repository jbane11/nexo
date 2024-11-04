#HV_logfile_ana

#Imports
import matplotlib.pyplot as plt
import os,sys,argparse,time,math
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
    
   



def main(Args):
    ''' Main script for doing work'''
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



    for line in infile.readlines()[-100::1]:


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

        #if eventtype=="new":
            #New Event
            #Need to append arrays and insert parameter
            # Channel_list[int(ch)].append_to_parameter("Time",[timestamp])
            # Channel_list[int(ch)].append_to_parameter(par,[val])



    if debug >9: #Debug for after the loop check
        print("\n\n\t\tAfter loop debug")
        for channel in Channel_list:
            for parameter in parameter_list:
                print(channel.name,f'{parameter:9}', ":", len(channel.get_parameter(parameter)))

    return Channel_list        


def plot_all_channels_2d(channels: list):
    """Plots 2D subplots for each parameter in each channel."""
    # Determine the number of parameters across all channels
    num_parameters = sum(len(channel.parameters) for channel in channels)
    
    # Set up a 2D grid with 2 columns (you can adjust the number of columns)
    cols = 4
    rows = math.ceil(num_parameters / cols)

    # Create subplots grid (rows x cols)
    fig, axs = plt.subplots(rows, cols, figsize=(12, 5 * rows))

    # Ensure axs is a 2D array even if there's only one row
    axs = axs.flatten()  # Flatten to make it easier to index

    plot_idx = 0
    for channel in channels:
        for parameter_name, time_value_pairs in channel.parameters.items():
            # Extract times and values
            times = [t[0] for t in time_value_pairs]
            values = [t[1] for t in time_value_pairs]

            # Plot in the corresponding subplot
            axs[plot_idx].plot(times, values, marker='o', linestyle='-', label=parameter_name)
            axs[plot_idx].set_title(f'{channel.name}: {parameter_name} vs Time')
            axs[plot_idx].set_xlabel('Time')
            axs[plot_idx].set_ylabel(parameter_name)
            axs[plot_idx].legend()
            axs[plot_idx].grid(True)
            axs[plot_idx].tick_params(axis='x', rotation=45)

            plot_idx += 1

    # Remove empty subplots if any
    if plot_idx < len(axs):
        for i in range(plot_idx, len(axs)):
            fig.delaxes(axs[i])

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()










if __name__ == "__main__":
    Args=argumentparse(sys.argv[1:])
    print(Args)
    Channel_list=main(Args)


    plot_all_channels_2d(Channel_list)





