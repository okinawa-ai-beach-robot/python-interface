#!/bin/env bash

# Check if external monitor connected and turned on:
connected=$(xrandr | awk '/ connected/ {count++} END {print count}')

if [ "$connected" -gt 1 ] && [ "$wallpaper" == "'zoom'" ]; then
echo "Monitor is connected!"
# Tasks todo when a monitor is connected (we are in OIST):
# 1. connect to oist WIFI (turn off hotspot and turn on again -> then trick to click on "accept")
# 2. update time from server!
else
echo "Monitor not conected -> Robot is in the wild!"
# Tasks todo:
# 1. start robot server
# 
fi


