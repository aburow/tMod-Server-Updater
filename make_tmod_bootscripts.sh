#!/bin/bash
cd /root
rm tModBootScripts.tgz
tar -czvf tModBootScripts.tgz tModLoader/boot_start.sh tModLoader/start.sh tModLoader/serverconfig.txt
