#HV_logfile_ana

#Imports
import os,sys,argparse,time
import matplotlib as plt
import pandas as pd


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

    # Parse the arguments
    args = parser.parse_args()
    return args


def openlogfile(Args):
    logfile_path=Args.logfilebase+Args.logfilename

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
 
    freshstep=0
    
    Event_list=[]
    Channel_list=[Channel(0),Channel(1),Channel(2),Channel(3)]
    parameter_list=["Time","VMon","IMonL","IMonH","VSet","ISet","ChStatus"]

    #Build up channels and parameters
    for channel in Channel_list:
        for parameter in parameter_list:
            channel.add_parameter(parameter,[0.0])

    #Number of unique time stamps
    event_count=1


    for line in infile.readlines()[0:2]:

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
            print("\n\tFirst Event")
            print("\t",ch,par,val)
            Channel_list[int(ch)].append_to_parameter(par,[val])
            Channel_list[int(ch)].append_to_parameter("Time",[timestamp])
            event_count+=1

       
            
            #SingleEvent=Event(struct_time,)

        elif freshstep==timestamp:
            print("\n\t\t\tRepeat event")
            print("\t\t\t",ch,par,val)
            Channel_list[int(ch)].append_to_parameter(par,[val])
            

            #Update parameters
        else:
            print("\n\t\tNewEvent")
            #append previous value all other parameters except time
            for channel in Channel_list:
                for parameter in parameter_list:
                    length=len(channel.get_parameter(parameter))
                    
                    if length!=event_count:
                        last_val=channel.get_parameter(parameter)[-1]
                        Channel_list[int(ch)].append_to_parameter(par,[last_val])
                    print(channel.name, parameter, length," :", channel.get_parameter(parameter))


            print("\t\t",ch,par,val)
            #Push all parameters
      
            Channel_list[int(ch)].append_to_parameter(par,[val])
            Channel_list[int(ch)].append_to_parameter("Time",[timestamp])
            
            #Update the comparison timestep
            freshstep=timestamp
            event_count+=1
        
        
        print("Event count ", event_count," \n\n")


        



        #Determine when the next time step changes
    print("\n\n\t\tAfter loop debug")
    for channel in Channel_list:
        for parameter in parameter_list:
            print(channel.name, parameter, " :", channel.get_parameter(parameter))





        





if __name__ == "__main__":
   Args=argumentparse(sys.argv[1:])
   print(Args)
   main(Args)







