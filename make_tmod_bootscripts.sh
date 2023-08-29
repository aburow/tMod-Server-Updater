#!/bin/bash

#
# Anthony Burow
# 
# This script is run manually to take a backup of the current server configs. This means
# that these files need to exist and they need to work as you want them to.
#
# This the archive is later used as a part of the upgrade process and is restored
# over the top of the top of the distrubuted defaults.
# 

cd /root
rm tModBootScripts.tgz
tar -czvf tModBootScripts.tgz tModLoader/boot_start.sh tModLoader/start.sh tModLoader/serverconfig.txt
