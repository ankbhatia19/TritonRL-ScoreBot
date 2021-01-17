import requests
import json
import os
import time


# Initialize API configuration 
DATA_PARAMS = 'config/cfg.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param

cfg = load_params(DATA_PARAMS)

# Intialize API configuration variables
token = cfg['token']
url = 'https://ballchasing.com/api/v2/upload?visibility='
visibility = 'private'
headers = {'Authorization': token }

# Initialize storage variables 
uploads = {}
replay_paths = [] 
base_directory = os.getcwd()
replay_directory = str(os.getcwd()) + '\\' + 'replays' + '\\' 
replay_directory = replay_directory.replace('\\', '/')

# Find all the replay file names/locations
for file in os.listdir(replay_directory):
    if file.endswith(".replay"):
        replay_paths.append(file)

# Change directories, upload replays, then revert back to starting directory
os.chdir(replay_directory)
for replay in replay_paths:
    #time.sleep(1)
    file_location = replay
    data = {
        'file':(replay, open(replay, 'rb'), 'binary/octet-stream')
        }
    r = requests.post(url + visibility, headers=headers, files=data)
    result = json.loads(r.content)
    uploads[result['id']] = result['location']
os.chdir(base_directory)


print(uploads)

with open("upload_data.json", "w") as outfile:  
    json.dump(uploads, outfile) 
