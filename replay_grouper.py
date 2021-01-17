import requests
import json


DATA_PARAMS = 'config/cfg.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param

cfg = load_params(DATA_PARAMS)

# Intialize API configuration variables
token = cfg['token']
url = 'https://ballchasing.com/api/replays/'
headers = {'Authorization': token}

# The name of the group to which we will be patching the replays
# Winter 
# patch_info = { 'group': 'ucsd-triton-rl-fall-2020-1isd8xduyl' }
patch_info = { 'group': 'ucsd-triton-rl-winter-2021-hdom9vwue2' }
# requests.patch seems to not convert the data to json automatically so I do it manually here
payload = json.dumps(patch_info)

# Load in the uploaded_data from file
with open("data/upload_data.json", "r") as read_file:
    #print("Converting JSON encoded data into Python dictionary")
    upload_data = json.load(read_file)


for replay_id in upload_data.keys():
    r = requests.patch(url + replay_id, headers=headers, data=payload)

# All of the replays should now be found in the specified UCSD Triton RL group
print('Done')