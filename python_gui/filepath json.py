import json

raw_config = {"base_path":"C:/Users/jasonbane/Desktop/nexo_code/Run Data (GUI v1)", 
              "filename":"RunList.csv",
              "ringdata":"ring.txt",
              "userinput":"user_data.txt"}

filepath_json = json.dumps(raw_config, indent=4)

with open("fileconfig.json", "w") as outfile:
    outfile.write(filepath_json)

