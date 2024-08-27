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
    def __init__(self, name):
        self.name = name
        
        self.parameters = {
            "VSet": 0,
            "ISet": 0,
            "ChStatus": 0,
            "power": 0,
            "VMon":0,
            "IMonL":0,
            "IMonH":0,    
        }
    # Initialize history as an empty list of dictionaries
        self.history = []
    #Set all the setting parameters  
    def newsets(self,vset,iset,status,power): 
                
        self.parameters = {
            "vset": vset,
            "iset": iset,
            "status": status,
            "power": power,
        }

                   

    def update_parameter(self, parameter, value, timestamp):
        """Update a parameter and store the change in history."""
        if parameter in self.parameters:
            # Save the current state to history before updating
            self.history.append({
                "time": timestamp,
                "parameter": parameter,
                "old_value": self.parameters[parameter],
                "new_value": value,
            })
            # Update the parameter
            self.parameters[parameter] = value
            print(f"Updated {parameter} to {value} at time {time.strftime('%Y-%m-%dT%H:%M:%S',timestamp)}")
        else:
            raise ValueError(f"Parameter '{parameter}' not recognized.")

    def get_history(self):
        """Return the history of changes."""
        return self.history

    def __str__(self):
        params = ", ".join([f"{k}: {v}" for k, v in self.parameters.items()])
        return f"Channel '{self.name}' with parameters: {params}"


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


    for line in infile.readlines()[0:5]:

        line_elements=line.split(" ")

        raw_timestamp=line_elements[0].replace("[","").replace("]","").replace("T"," ")
        # Convert the string to a struct_time object
        struct_time = time.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S:")
        # Convert the struct_time object to a timestamp (seconds since the epoch)
        timestamp = time.mktime(struct_time)
    
        #Grab channel, parameter and value
        print(line_elements)
        ch=line_elements[5][1:-1]
        par=line_elements[7][1:-1]
        val=line_elements[9][1:-2]
        print(ch,par,val)

        

        if freshstep==0:
            freshstep=timestamp
            print("\n\tFirst Event")
            #Inilaize parameters and new timestep   
            Channel_list[int(ch)].update_parameter(par,val,struct_time)
            
            #SingleEvent=Event(struct_time,)

        elif freshstep==timestamp:
            print("\n\t\t\tRepeat event")
            
            

            #Update parameters
        else:
            print("\n\t\tNewEvent")
            for ch in Channel_list:
                ch.get_history()
            
            
            #Push all parameters
            #Update the comparison timestep
            freshstep=timestamp




        #Determine when the next time step changes






        





if __name__ == "__main__":
   Args=argumentparse(sys.argv[1:])
   print(Args)
   main(Args)







