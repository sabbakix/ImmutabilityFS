#!/usr/bin/env python3

import os
import subprocess
import re
import datetime

def is_immutable(pathfile):
    result = subprocess.run(["lsattr", pathfile ], shell=False, capture_output=True, text=True)
    if result.stdout[4] == "i":
        return True
    else:
        return False

def set_immutable(pathfile):
    result = subprocess.run(["chattr", "+i", pathfile], shell=False, capture_output=True, text=True)
    #print("stout: ",result.stdout)
    result2 = subprocess.run(["lsattr", pathfile ], shell=False, capture_output=True, text=True)
    #print(result2.stdout)

def is_dir(pathfile):
    if os.path.isdir(pathfile):
        return True
    else:
        return False

def get_paths_from_vbm(pathfile):
    if pathfile[-4:] == ".vbm":
        with open(pathfile, "r") as file:
            data = file.read()
            # Modified regex to capture the timestamp as well
            regex = r'FilePath="(.*?)(\d{4}-\d{2}-\d{2}T\d{2}\d{2}\d{2})(\.vbk|\.vib)"'
            matches = re.findall(regex, data)
                        
            # Convert matches to a list of tuples (path, timestamp)
            matches_with_timestamp = []
            for match in matches:
                #print(match[0]+match[1]+match[2])
                path_from_file = match[0]+match[1]+match[2]
            
                # Parse the timestamp into a datetime object
                timestamp = datetime.datetime.strptime(match[1], "%Y-%m-%dT%H%M%S")
                matches_with_timestamp.append((path_from_file, timestamp))

            # Sort the list by timestamp
            sorted_matches = sorted(matches_with_timestamp, key=lambda x: x[1])
            
            # Optionally, if you only need the paths in sorted order:
            sorted_paths = [match[0] for match in sorted_matches]
            
            # Print the sorted paths for verification
            for path in sorted_paths:
                print("Sorted path: ", path)
            
            # Assuming sorted_paths is already defined and populated
            last_sorted_path = sorted_paths[-1] if sorted_paths else None

            print("Last sorted path:", last_sorted_path)
            
            return sorted_paths
    else:
        print("no .vbm")


path="/POOL2/Z14/B14/OMEGA_PC_HP_PROBOOK_470_G0_WIN10"
dir_list = os.listdir(path)


for entry in dir_list:
    pathfile = path+"/"+entry
    #print("imm: ",is_immutable(path+"/"+entry)," ext:",entry[-4:], " "+entry)

    if is_dir(pathfile): #is dir
        pass
    else: # is file
        if  entry[-4:] == ".vbm":
            vbm_paths_list = get_paths_from_vbm(pathfile)
        else:
            set_immutable(pathfile)

