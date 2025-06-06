import h5py
import time

def get_data(file_path):
    def safe_h5_open(path, mode='a', retries=5, delay=0.2):
        for attempt in range(retries):
            try:
                return h5py.File(path, mode)
            except BlockingIOError:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise

    with safe_h5_open(file_path, mode='r') as f:
        data = {}
        data['run'] = {}
        for group in f['run'].keys():
            data['run'][group] = {}
            for dataset in f['run'][group].keys():
                data['run'][group][dataset] = f['run'][group][dataset][:]
            
            data['run'][group]['metadata'] = {}
            for attr in f['run'][group].attrs.keys():
                data['run'][group]['metadata'][attr] = f['run'][group].attrs[attr]
        
        data['pid_info'] = {}
        for dataset in f['pid_info'].keys():
            data['pid_info'][dataset] = f['pid_info'][dataset][:]
        
        data['omb_daq'] = {}
        for dataset in f['omb_daq'].keys():
            data['omb_daq'][dataset] = f['omb_daq'][dataset][:]

        data['tc08_daq'] = {}
        for dataset in f['tc08_daq'].keys():
            data['tc08_daq'][dataset] = f['tc08_daq'][dataset][:]
            
    return data