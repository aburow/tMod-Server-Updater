#!/bin/bash

# Anthony Burow
# 
# This file sets up tmux for tmod to run in the background on a virtual terminal
# The file is meant to be called from crontab after every restart of an LXC
#
# called by: crontab
# calls: start.sh

tmux new -d -s tmod
tmux send-keys -t tmod:. "cd /root/tModLoader" C-m
tmux send-keys -t tmod:. "./start.sh boot" C-m
