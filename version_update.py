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
import shutil
import json

"""I use the following variables to cache the answers that I get from various 
calls. Technically, the application can be written to use live calls as 
needed but I was trying to be more efficient and prevent getting download 
blocks during the development cycle."""
newVersion = ""
oldVersion = ""

# globals :|

IMAGE_URL = "https://github.com/tModLoader/tModLoader/releases/latest"
LOG_FILE = "/root/tModLoader/tModLoader-Logs/server.log"


def get_latest_version() -> str:
    """Returns the latest version of tmodloader from the official Github
        releases page.

    Calls are pointed to a redirection page at Github, a URL is passed back
    and the end of the URL gives the latest version number.
    """
    r = requests.get("https://github.com/tModLoader/tModLoader/releases/latest")
    return r.url.split("/v")[-1]  # last part is the version


def get_installed_version() -> str:
    """Returns the currently installed version of tmodloader.

    This function looks at the first line of the logfile and extracts the
    version number.
    """
    try:
        with open("version_update.json", "r") as vu:
            jvu = json.load(vu)
            version = jvu.get("version")
            if version is not None:
                return version

    except FileNotFoundError:
        print("version_update.json not found")

    with open(LOG_FILE, "r") as f:
        first_line = f.readline().strip("\n").split("+")
        version_is = first_line[1].split("|")
    return version_is[0]  # first part is the version


def version_compare(new_version: str, old_version: str) -> bool:
    """Takes in two strings and compares them to see if they are different,
        if they're different True is returned.
    """
    if new_version != old_version:
        return True  # There is a new release
    return False  # No new release


def backup_execs(id_name: str) -> ...:
    """Does a full backup of the current running server executables in-situ.

    The backup can be restored directly back into the original directory or
    copied to another server for deployment.

    Parameters:
        id_name (str): The identifier you want to use to differentiate
            between multiple backups, e.g. the version number.

    Returns:
        Nothing intelligible at the moment. ahem I mean, not implemented.
    """
    shutil.make_archive(f"./tMod-execs-{id_name}", "gztar",
                        "/root/", "tModLoader")
    result = shutil.move(f"./tMod-execs-{id_name}.tar.gz",
                         "./backup")
    return result


def backup_datafiles(id_name: str) -> ...:
    """Does a full backup of the current servers data files, including maps and
        plugins.

    Parameters:
        id_name (str): The identifier you want to use to differentiate
            between multiple backups, e.g. the version number.

    Returns:
        Nothing intelligible at the moment. ahem I mean, not implemented.
    """
    shutil.make_archive(f"./tMod-datafiles-{id_name}",
                        "gztar", "/root/",
                        ".local/share/Terraria")
    result = shutil.move(f"./tMod-datafiles-{id_name}.tar.gz",
                         "./backup")
    return result


def move_current_dir(version_number: str) -> None:
    """Renames the "tModLoader" directory to the format "tModLoader-v{
        version_number}"

    Parameters:
        version_number (str): The version number.
    """
    result = os.rename("tModLoader", f"tModLoader-v{version_number}")
    return result


def make_new_dir() -> None:
    """Makes a new "tModLoader" directory.
    """
    result = os.mkdir("tModLoader")
    return result


def get_latest_zip(version: str) -> str:
    """Gets the requested version of the tModLoader installation files.

    Parameters:
        version (str): The version that you want to download.
    """
    image_file = ("https://github.com/tModLoader/tModLoader/releases/download/"
                  f"v{version}/tModLoader.zip")
    result = wget.download(image_file,
                           out=f"tModLoader/tModLoader-v{version}.zip")
    return result


def server_setup(version: str):
    """Unpack the server distribution zip.

    Precondition:
        The version is already downloaded and in the expected location.

    Parameters:
        version (str): The version you are unpacking.
    """
    image_file = f"tModLoader/tModLoader-v{version}.zip"
    extract_dir = "/root/tModLoader"
    result = shutil.unpack_archive(image_file, extract_dir)
    return result


def deploy_startfiles():
    """Redeploy config and startup shell files to new directory structure.
    """
    image_file = "tModBootScripts.tgz"
    result = shutil.unpack_archive(image_file)
    return result


# main-loop
if __name__ == '__main__':
    print("Start Check")
    oldVersion = get_installed_version()
    newVersion = get_latest_version()
    print(f"Latest Release    : {newVersion}")
    print(f"Installed Release : {oldVersion}")
    print(f"Update Status     : {version_compare(newVersion, oldVersion)}")
    if newVersion != oldVersion:
        print(f"Backup Executables: ", end='')
        print(backup_execs(oldVersion))
        print("Backup Data Files : ", end='')
        print(backup_datafiles(oldVersion))
        print("Move Current Inst.: ", end='')
        print(move_current_dir(oldVersion))
        print("Prepare Directory : ", end='')
        print(make_new_dir())
        print("Retrieve File     : ", end='')
        print(get_latest_zip(newVersion))
        print("Unzip New Server  : ", end='')
        print(server_setup(newVersion))
        print("Deploy Start Files: ", end='')
        print(deploy_startfiles())
        print("You can now reboot")

