#!/bin/bash
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
