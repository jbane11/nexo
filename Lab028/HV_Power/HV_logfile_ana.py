#HV_logfile_ana

#Imports
import os,sys,argparse,time
import numpy as np
import matplotlib as plt
import pandas as pd
parameter_list=["Time","VMon","IMonL","IMonH","VSet","ISet","ChStatus"]
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
            channel.add_parameter(parameter,["0.0000"])

    #Number of unique time stamps
    event_count=1



    for line in infile.readlines()[0:20]:

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
        

        if freshstep==0:
            freshstep=timestamp
            if debug >= 6: print("\n\tFirst Event")
            if debug >= 8: print("\t",ch,par,val)
            Channel_list[int(ch)].append_to_parameter(par,[val])
           #Add timestep to each channel
            Channel_list[int(0)].append_to_parameter("Time",[timestamp])
            Channel_list[int(1)].append_to_parameter("Time",[timestamp])
            Channel_list[int(2)].append_to_parameter("Time",[timestamp])
            Channel_list[int(3)].append_to_parameter("Time",[timestamp]) 
            event_count+=1

       
            
            #SingleEvent=Event(struct_time,)

        elif freshstep==timestamp:
            if debug >= 6:print("\n\t\t\tRepeat event")
            if debug >= 8:print("\t\t\t",ch,par,val,raw_timestamp)
            Channel_list[int(ch)].append_to_parameter(par,[val])
            

            #Update parameters
        else:
            if debug >= 6: print("\n\t\tNewEvent")
            #append previous value all other parameters except time
            for channel in Channel_list:
                for parameter in parameter_list:
                    length=len(channel.get_parameter(parameter))
                    ijk=0
                    while length<event_count:
                    
                        last_val=channel.get_parameter(parameter)[-1]
                        if debug >= 10:print(f"\t\t: add {last_val:} to {parameter}, channel: {channel.name}")
                        channel.append_to_parameter(parameter,[last_val])
                        length=len(channel.get_parameter(parameter))
                        print(f"Test {ijk}, Length :: {length} :: EC {event_count}")
                        ijk=+1#print(channel.name, parameter, length)
                    
                    
                    if length < event_count*-2:                        #print(channel.name, parameter)
                        last_val=channel.get_parameter(parameter)[-1]
                        if debug >= 10:print(f"\t\t add {last_val} to {parameter}, channel: {channel.name}")
                        channel.append_to_parameter(parameter,[last_val])
                    
                    length=len(channel.get_parameter(parameter))
                    if debug >= 10:print("\t",channel.name, parameter, length," :")#, channel.get_parameter(parameter))


            if debug >= 8: print("\n\n INFO::",ch,par,val)
            #Push all parameters
      
            Channel_list[int(ch)].append_to_parameter(par,[val])
            Channel_list[int(ch)].append_to_parameter("Time",[timestamp])

          
            #Update the comparison timestep
            freshstep=timestamp
            event_count+=1


        
        if debug >= 4: print("\nEvent count ", event_count," \n")



   #######End of logfile
    print("Last bin")            
    for channel in Channel_list:
        for parameter in parameter_list:
            length=len(channel.get_parameter(parameter))
            print(channel.name, parameter, length)
            ijk=0
            while length<event_count:
            
                last_val=channel.get_parameter(parameter)[-1]
                if debug >= 10:print(f"\t\t add {last_val:} to {parameter}, channel: {channel.name}")
                channel.append_to_parameter(parameter,[last_val])
                length=len(channel.get_parameter(parameter))
                print(f"Test {ijk}")
                ijk=+1

    
    

    if debug >9: #Debug for after the loop check
        print("\n\n\t\tAfter loop debug")
        for channel in Channel_list:
            for parameter in parameter_list:
                print(channel.name,f'{parameter:9}', ":", channel.get_parameter(parameter))

    return Channel_list



def MakeDataFrame(Channel_list):

    DFs=[]
    for i in [0,1,2,3]:
        DF=pd.DataFrame()
        
        for parameter in parameter_list:
            print(parameter,len(Channel_list[int(i)].get_parameter(parameter)))
            DF[parameter] = np.array(Channel_list[int(i)].get_parameter(parameter))





    













        





if __name__ == "__main__":
   Args=argumentparse(sys.argv[1:])
   print(Args)
   Channel_list=main(Args)
   MakeDataFrame(Channel_list)






