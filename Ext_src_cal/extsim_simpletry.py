import import_ipynb
#from nexoheader import *

import uproot 
import uproot3
import uproot4
import awkward as ak


rootdir = "./data"
recondir = "./data"
file_name_conv="Config-verison-iso-nevts-seed#(_type).root"



def file_info_from_file(file):
    #fdata=file.find("data")
    #file=file[fdata:]
    
    try:
        first_dash=file.find("-")
        last_slash=file.rfind("/")
        Config=file[last_slash+1:first_dash]
        file=file[first_dash+1:]
    except:
        print("Issue with Config")
        exit()
    try:
        version="0"
        if file.find("v")>=0:
            version_dash=file.find("-")
            version=file[:version_dash]
            file=file[version_dash+1:]
        else:
            verison="0"
    except:
        print("issue with version")
        exit()
    try:
        tgt_dash=file.find("-")
        tgt=file[:tgt_dash]
        file=file[tgt_dash+1:]

        evts_dash=file.find("-")
        numevents=int(file[:evts_dash])
        seed=file[file.find("seed")+4:file.find(".")]
    except:
        print("issue with seed or numevents")
        return 0,0,0,0,0
        
    return Config,tgt,numevents,seed,version

def file_dict_from_file(file):
    
    fileinfo=file_info_from_file(file)
    
    fi=fileinfo
    if fileinfo[0] == 0:
        print("Double check file name")
        print("Recall: naming convention : %s "%file_name_conv)
        
        return False
    
    simFiledict={}
    simFiledict["Config"]=fileinfo[0]
    simFiledict["Target"]=fileinfo[1]
    simFiledict["NumEvents"]=fileinfo[2]
    simFiledict["Seed"]=fileinfo[3]
    simFiledict["Version"]=fileinfo[4]
    simFiledict["root_filename"]="%s/%s-%s-%s-%s-seed%s.root"%(rootdir,
                                                                                           fi[0],
                                                                                           fi[4],
                                                                                           fi[1],
                                                                                           fi[2],
                                                                                           fi[3])
    
    simFiledict["sens_filename"]="%s/%s-%s-%s-%s-seed%s_sensrecon.root"%(recondir,
                                                                                           fi[0],
                                                                                           fi[4],
                                                                                           fi[1],
                                                                                           fi[2],
                                                                                           fi[3])
    
    
    return simFiledict









sens_Treenames=["Event/Recon/Energy/Energy","Event/Recon/Standoff/Standoff"
                ,"Event/Recon/ChargeQuanta/ChargeQuanta","Event/Recon/Photons/Photons"
                ,"Event/Recon/DNNTag/DNNTag","Event/Recon/NESTBugFlag/NESTBugFlag"]
root_Treenames=["Event/Sim/SimEvent"]
root_bnames=["fGenX"
                ,"fGenY"
                ,"fGenZ"
                ]


newfilename="./data/Bi212_v3_seed10.root"
file="./data/ExternalGammas_light-v3-Bi212-5000-seed10.root"


#def SimpleComb(file,newfile)
if 1==1:
    
    
    FI=file_dict_from_file(file)

    
    ReconFile=uproot4.open(FI["sens_filename"])
    MainReconKeys=ReconFile["Event/Recon"].keys()    

    ReconDict={}
    ReconDictInfo={}

    for i, Full_bname in enumerate(sens_Treenames):
        
        Short_bname=Full_bname.split("/")[-1]
        leaves=ReconFile[Full_bname+"/"+Short_bname].keys()[4:]
        
        for leaf in leaves:
            ReconDict[leaf]=ReconFile[Full_bname+"/"+Short_bname+"/"+leaf].array()
            ReconDictInfo[leaf]=type(ReconDict[leaf][0])



    ReconFile.close()


    with uproot3.recreate(newfilename) as f:
        f["nexo"] = uproot3.newtree(ReconDictInfo,title="")

        f["nexo"].extend(ReconDict,flush=False)
    
    f.close()

    


    #G4File=uproot4.open(file)
    #G4File.close()





