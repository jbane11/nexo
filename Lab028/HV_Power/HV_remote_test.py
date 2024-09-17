from caen_libs import caenhvwrapper as hv  
from pycaenhv.wrappers import init_system, deinit_system, get_board_parameters, get_crate_map, get_channel_parameter_property, get_channel_parameters, list_commands,get_channel_parameter
from pycaenhv.enums import CAENHV_SYSTEM_TYPE, LinkType
from pycaenhv.errors import CAENHVError
import os, time


type="N1470"   ##Type of power suppl
link="USB_VCP" ##How the supply is connected
address="COM10"   ##The connection port


def connect():
    system_type = CAENHV_SYSTEM_TYPE[type] #Function to pull enum from list of types
    link_type = LinkType[link]             #Function to pull enum from list of links

    try:
        deinit_system(handle)
    except:
        print("System already closed")

    # Make connection  
    print("Opening connection")
    try:
        handle = init_system(system_type, link_type,
                            address,
                            '','')
    except:

        print("issue with connection")
        exit()

    try:
        print(f"Got handle: {handle}")
        crate_map = get_crate_map(handle)
        for name, value in crate_map.items():
            print(name, value)
        board_parameters = get_board_parameters(handle, 0)
    except CAENHVError as err:
        print(f"Got error: {err}\nExiting ...")

    return(handle)




def deint(handle):
    try:
        deinit_system(handle)
    except:
        print("Issue with closing connection")


if __name__ == '__main__':

    handle=connect()

    ch_keys=get_channel_parameters(handle,0,0)

    Go=True
    counter=0

    while(Go):
        
        printstr="%i "%(counter)
        for key in ch_keys:
            printstr= printstr + "%s %s, "%(key, get_channel_parameter(handle,0,1,key))


        print(printstr)

        counter+=1
        if counter>=5:
            Go=False
        time.sleep(1)


    deint(handle)        


