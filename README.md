# tMod-Server-Update
Script to backup, deploy new version of tMod on existing installation

Installation/Requirements:

      We run the system in a protected container and these instructions are for
      the instances that we run but should work with any other system. You still
      need to do the setup for "serverconfig.txt" because we wrote this app for
      our already running servers.

      Start by doing some additional installs to prepare the environment.

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

          After these 2 files are created, make the shellscipts in the directory
          executable: 'chmod +x /root/tModLoader/*.sh'

          To restart the tMod server automatically after reboot:

              To edit crontab use the following:
                  crontab -e

              Then add the following line to the bottom of the crontab file:
                  @reboot /root/tModLoader/boot_start.sh

Install and Run the code:
      Install "version_update" into the directory under tModServer. In containers
      this may well be /root/ make version_update executable with 'chmod +x version_update'

      Before running the program the first time you MUST have a working tModLoaderServer
      that is operating as the program gets the current version from the server logfiles.
      
      On the first run execute "version_update" without any parameters. This will provide
      you with a usage output and will setup the version_upgrade.json file which to make version
      tracking easier going forward. The first run will show an error above the usage information.

      Currently there are only two commands available:
      version_update check      :      Checks whether there is a new version of tModLoader
                                       and outputs the results.
      version_update upgrade    :      Check whether the installed version is same as current
                                       Takes a backup of data and server files into ./backup
                                       Creates a fresh install in ./tModLoader
                                       Pulls old config from the previous install

      Version update will provide exit codes so that it can be included in automations and
      additional scripts to for administrative tasks.

Exit Codes:
       0: Exit without error | no upgrade available | upgrade successful
       2: No parameters or valid commands
      42: New version available
      69: File move and copy errors detected
      88: All other errors

