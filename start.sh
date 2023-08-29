#!/bin/bash

# Anthony Burow
# 
# This script does the following when called from 'boot_start.sh':
#   1. Delays the start sequence to allow the booting LXC container to stabilise with all services ready. (15 sec default)
#   2. makes all shell scripts unzipped from tModServer archive executable
#   3. creates a loop to run tModLoaderServer.sh
#      a. if the server crashes or the server is shutdown the script waits 5 seconds and loads the server again.
#      b. The script prompts for CTRL+C to let the admin know when they can safely break out of the script
#
#  When the script is started from "boot_script.sh" it is called as "start.sh boot" in order to add the start delay
#  If the script is run without the "boot" parameter there is no delay. This allows a start from the cli on a fully
#  loaded and stabilised container or server
#
#  calls: start-tModLoaderServer.sh
#  info:
#  -nosteam  =  Loads the tMod server without the steam libraries and login
#  -noupnp   =  Disables uPNP from setting up inbound TCP NAT conduits on upstream routers public internet interface
#

if [[ $1 == "boot" ]]
then
  sleep 15
fi

while :
do
        cd /root/tModLoader
        chmod 755 *.sh
        ./start-tModLoaderServer.sh -nosteam -noupnp
        echo "Press [CTRL+C] to stop.."
        sleep 5
done
