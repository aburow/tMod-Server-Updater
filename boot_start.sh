#!/bin/bash
tmux new -d -s tmod
tmux send-keys -t tmod:. "cd /root/tModLoader" C-m
tmux send-keys -t tmod:. "./start.sh boot" C-m
