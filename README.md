# tMod-Server-Update
Script to backup, deploy new version of tMod on existing installation

Installation/Requirements:

      I run the system in a protected container and these instructions are for
      the instances that I run but should work with any other system. You still
      need to do the setup for "serverconfig.txt" because I wrote this app for
      my already running servers.

      Start by doing some additional installs.

          apt-get install tmux

          Install the following python libraries with:
              pip3 install requests wget shutils

          create a directory /root/backup

          create boot_start.sh as follows in /root/tModLoader/

                    #!/bin/bash
                    tmux new -d -s tmod
                    tmux send-keys -t tmod:. "cd /root/tModLoader" C-m
                    tmux send-keys -t tmod:. "./start.sh boot" C-m

          create start.sh as follows in /root/tModLoader/

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

          After these 2 files are created, make them executable: 'chmod +u /root/tModLoader/*.sh'

          Make the startup config backup and restore file "tModBootScripts.tgz" in /root
          This file is important to make your config startable across build updates.
          Build the file with:
              cd /root
              "tar -czvf tModBootScripts.tgz tModLoader/boot_start.sh tModLoader/start.sh tModLoader/serverconfig.txt"

          To restart the tMod server automatically after reboot:

              To edit crontab use the following:
                  crontab -e

              Then add the following line to the bottom of the crontab file:
                  @reboot /root/tModLoader/boot_start.sh
