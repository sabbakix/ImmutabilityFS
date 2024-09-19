#!/usr/bin/env python3

import os
import re
import time
import shutil
import subprocess
from sys import exit
from data import imfolders
from datetime import datetime, timedelta




# path : time frame
list_of_veeam_folder_to_protect = imfolders()

def is_immutable(pathfile):
    result = subprocess.run(["lsattr", pathfile ], shell=False, capture_output=True, text=True)
    #print("def is_immutablestout: ",result.stdout)
    if result.stdout[4] == "i":
        return True
    else:
        return False
    
def get_backup_chain(filepath):
    """
    Get the backup chain for a given file, filtering out non-backup files.
    
    Args:
        filepath (str): The path to the file.
    
    Returns:
        list: A sorted list of backup files (.vbk, .vib, .vbm, .vbm.off) in the same directory.
    """
    # Get the directory of the file
    directory = os.path.dirname(filepath)
    # Get the name of the file
    filename = os.path.basename(filepath)
    
    # Check if the file is a .vbk, .vib, .vbm, or .vbm.off file
    if filename.endswith(('.vbk', '.vib', '.vbm', '.vbm.off')):
        # Get the list of files in the directory
        files = os.listdir(directory)
        # Sort the files
        files.sort()
        
        # Initialize an empty list to store backup files
        backup_files = []
        
        # Iterate over the files and filter out non-backup files
        for file in files:
            if file.endswith('.vbk'):
                backup_files.append(file)
            elif file.endswith('.vib'):
                backup_files.append(file)
            elif file.endswith('.vbm'):
                backup_files.append(file)
            elif file.endswith('.vbm.off'):
                backup_files.append(file)
        
        backup_files.sort()

        return backup_files
    else:
        return []
'''
files = get_backup_chain("/POOL2/Z14/B14/OMEGA_PC_HP_PROBOOK_470_G0_WIN10/OMEGA_PC_HP_PROBOOK_470_G0_WIN102024-09-15T014701.vib")
print(files)
exit()

'''


def len_of_vbk_vib_immutable(veeam_folder):
    n_immutable = 0
    for file in veeam_folder:
        if file[-4:] == ".vbk" or file[-4:] == ".vib":
            if is_immutable(file):
                n_immutable = n_immutable + 1
    return n_immutable
    
    
def set_immutable(pathfile):
    result = subprocess.run(["chattr", "+i", pathfile], shell=False, capture_output=True, text=True)
    #print("stout: ",result.stdout)
    pass

def set_mutable(pathfile):
    result = subprocess.run(["chattr", "-i", pathfile], shell=False, capture_output=True, text=True)
    #print("stout: ",result.stdout)
    pass

def is_dir(pathfile):
    if os.path.isdir(pathfile):
        return True
    else:
        return False

def get_file_time(file_path):
    # Get file stats
    stats = os.stat(file_path)
   
    # Extract last modified time and format it
    modified_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%dT%H%M%S')
    
    return modified_time

def get_file_size(file_path):
    # Get file stats
    stats = os.stat(file_path)
    
    # Extract size in bytes
    size = stats.st_size

    return size


def is_older_than_days(timestamp, days = 30):
    # Define the format for the timestamp
    format_str = "%Y-%m-%dT%H%M%S"
    
    # Convert the string timestamp to a datetime object
    datetime_obj = datetime.strptime(timestamp, format_str)
    
    # Get the current datetime
    now = datetime.now()
    
    # Calculate the difference between the current datetime and the timestamp
    delta = now - datetime_obj
    
    # Check if the difference is more than 30 days
    return delta > timedelta(days)

def get_veeam_files_from_veeam_folder(veeam_folder):
    veeam_file_list = []
    list_of_files_and_dirs = os.listdir(veeam_folder)
    for entry in list_of_files_and_dirs:
        full_path_to_file = veeam_folder+"/"+entry
        if not is_dir(full_path_to_file): # is file
            if  entry[-4:] == ".vbk" or entry[-4:] == ".vib" or entry[-4:] == ".vbm" or entry[-8:] == ".vbm.off":
                veeam_file_list.append(full_path_to_file)
    veeam_file_list.sort()
    return veeam_file_list


def is_backup_running(veeam_folder):
    veeam_files = get_veeam_files_from_veeam_folder(veeam_folder)
    vbm_file_path = ""
    vbm_time= ""
    last_vbk_vib_path = ""
    last_vbk_vib_time = ""
    veeam_files.sort()
    for file in veeam_files:
        print(file)
        if file[-4:] == ".vbm":
            vbm_file_path = file
            vbm_time = get_file_time(file)
        elif file[-8:] == ".vbm.off":
            pass
        elif file[-4:] == ".vbk" or file[-4:] == ".vib":
            last_vbk_vib_path = file
    last_vbk_vib_time = get_file_time(last_vbk_vib_path)
    times = []
    times.append(vbm_time+".vbm")
    times.append(last_vbk_vib_time)
    times.sort()

    print("vbm_file_path:",vbm_file_path)
    print("vbm_time:", vbm_time)
    print("last_vbk_vib_path:",last_vbk_vib_path)
    print("last_vbk_vib_time:",last_vbk_vib_time)
    print(times)
    
    
    
    is_the_last_vbk_or_vib_changing_in_size = False
    size1 = get_file_size(last_vbk_vib_path)
    time.sleep(3)
    size2 = get_file_size(last_vbk_vib_path)
    if size1 == size2 :
        is_the_last_vbk_or_vib_changing_in_size = False
    else:
        is_the_last_vbk_or_vib_changing_in_size = True
    print("is_the_last_vbk_or_vib_changing_in_size:",is_the_last_vbk_or_vib_changing_in_size)

    if is_the_last_vbk_or_vib_changing_in_size:
        return True
    
    is_vbm_younger_than_3mins = True
    now = datetime.now()
    mod_time = datetime.fromtimestamp(os.path.getmtime(vbm_file_path))
    # Check if the file is older than 3 minutes
    if now - mod_time > timedelta(minutes=3):
        print(f"The file vbm is older than 3 minutes.")
        is_vbm_younger_than_3mins = False
    else:
        print(f"The file vbm is not older than 3 minutes.")
        is_vbm_younger_than_3mins = True

    if is_vbm_younger_than_3mins:
        return True
        
    is_vbm_the_last_file_modified = False
    last_elem = times[-1]
    if last_elem[-4:] == ".vbm":
        is_vbm_the_last_file_modified = True
    print("is_vbm_the_last_file_modified:", is_vbm_the_last_file_modified)
    if not is_vbm_the_last_file_modified:
        return True

 
def set_veeam_immutability(veeam_folder, days_of_immutability = 30):
    print("days of immutability:", days_of_immutability)
    if is_backup_running(veeam_folder):
        print("backup is running")
    else:
        print("backup is not running")
        # duplicate vbm and set immutability on .vbk .vib .off files
        veeam_files = get_veeam_files_from_veeam_folder(veeam_folder)

        len_veeam_files = len(veeam_files)

        # if .vbm duplicate vbm file ad set immutable
        # if .vbk and .vib set immutable
        vbm_file_path = ""
        for file in veeam_files:
            print(file," imm:",is_immutable(file))
            if file[-4:] == ".vbm":
                vbm_file_path = file
            else:
                # set immutable .vbk and .vib and .vbm.off files
                # set mutable and delete old files
                # print("protect time: ",get_file_time(vbm_file_path))
                # 
                
                
                print ("len imm:",len_of_vbk_vib_immutable(veeam_files))
                if len_of_vbk_vib_immutable(veeam_files) > days_of_immutability:
                    if is_older_than_days(get_file_time(file), days = days_of_immutability):
                        set_mutable(file)
                    else:
                        set_immutable(file)
                else:
                    set_immutable(file)

                
                

        source = vbm_file_path
        get_file_time(vbm_file_path)
        destination = vbm_file_path[:-4]+get_file_time(vbm_file_path)+".vbm.off"
        print("source:",source)
        print("destination:",destination)
        
        if not os.path.isfile(destination):
            shutil.copy2(source, destination)
            set_immutable(destination)
        else:
            print("destination already exists")

        




for veeam_folder in list_of_veeam_folder_to_protect.keys():
    print("veeam_folder:",veeam_folder)
    print("days:",list_of_veeam_folder_to_protect[veeam_folder])
    set_veeam_immutability(veeam_folder, days_of_immutability=list_of_veeam_folder_to_protect[veeam_folder])





