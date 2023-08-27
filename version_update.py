#!/usr/bin/python3
# Automatically update tmod server v0.01
# Anthony Burow - 26 August 2023
# apburow@hotmail.com
#
# License: GPL3
#
# This program has absolutely zero error checking
#

import requests
import wget
import os
# import sys
import shutil

'''
I use the following variables to cache the answers that I get from various calls. Technically, the application can
be written to use live calls as needed but I was trying to be more efficient and prevent getting download blocks
during the development cycle.
'''
newVersion = ""
oldVersion = ""

def get_latest_version():
    """
    This call is pointed at a redirection page at github. It is a cheaty way of getting the latest version of code
    if the authors have setup for this. A URL is passed back that I use to get the latest version number an return.
    """
    image_url = "https://github.com/tModLoader/tModLoader/releases/latest"
    r = requests.get(image_url)
    return r.url.split("/v")[-1]     # last part is the version

def get_installed_version():
    '''
    I wasn't able to find a good way to locate the current running version on the server. This little hack looks at
    first line of the logfile and extracts the tModLoader version. I return the version number.
    '''
    log_file = "/root/tModLoader/tModLoader-Logs/server.log"
    with open(log_file, 'r') as f:
        first_line = f.readline().strip('\n').split('+')
        version_is = first_line[1].split('|')
    f.close()
    return version_is[0]            # first part is the version

def version_compare(n,o):
    '''
    A dumb version compare. I put this into the application in stubby code and haven't removed it because I don't know
    if I really need it or not if I find better ways to deal with this in the future. The function takes in two
    variables and returns one of two values. It's not currently doing anything of great value.
    '''
    if (n != o):
        return "New Release Available"
    else:
        return "No New Release"

def backup_execs(o):
    '''
    Do a full backup of the current running server executables in-situ. The backup can be restored directly back into
    the original directory or copied to another server for deployment. The return at the moment is nonsense.
    '''
    result = shutil.make_archive(f"./tMod-execs-{o}","gztar","/root/","tModLoader")
    result = shutil.move(f"./tMod-execs-{o}.tar.gz","./backup")
    return result

def backup_datafiles(o):
    '''
    Do a full backup of the current servers data files, including maps and plugins. The return at the moment is
    nonsense.
    '''
    result = shutil.make_archive(f"./tMod-datafiles-{o}","gztar","/root/",".local/share/Terraria")
    result = shutil.move(f"./tMod-datafiles-{o}.tar.gz","./backup")
    return result

def move_current_dir(o):
    result = os.rename("tModLoader",f"tModLoader-v{o}")
    return result

def make_new_dir():
    result = os.mkdir("tModLoader")
    return result

def get_latest_zip(n):
    '''
    Gets the requested version of the tModLoader installation files
    '''
    image_file = f"https://github.com/tModLoader/tModLoader/releases/download/v{n}/tModLoader.zip"
    result = wget.download(image_file,out=f"tModLoader/tModLoader-v{n}.zip")
    return result

def server_setup(n):
    '''
    Unpack the server distribution zip
    '''
    image_file = f"tModLoader/tModLoader-v{n}.zip"
    extract_dir = "/root/tModLoader"
    result = shutil.unpack_archive(image_file, extract_dir)
    return result

def deploy_startfiles():
    '''
    Redeploy config and startup shell files to new directory structure
    '''
    image_file = "tModBootScripts.tgz"
    result = shutil.unpack_archive(image_file)
    return result

# main-loop
if __name__ == '__main__':
    print('Start Check')
    oldVersion = get_installed_version()
    newVersion = get_latest_version()
    print(f"Latest Release    : {newVersion}")
    print(f"Installed Release : {oldVersion}")
    print(f"Update Status     : {version_compare(newVersion,oldVersion)}")
    if ( newVersion != oldVersion ):
        print(f"Backup Executables: {backup_execs(oldVersion)}")
        print(f"Backup Data Files : {backup_datafiles(oldVersion)}")
        print(f"Move Current Inst.: {move_current_dir(oldVersion)}")
        print(f"Prepare Directory : {make_new_dir()}")
        print(f"Retrieve File     : {get_latest_zip(newVersion)}")
        print(f"Unzip New Server  : {server_setup(newVersion)}")
        print(f"Deploy Start Files: {deploy_startfiles()}")
        print(f"You can now reboot")
