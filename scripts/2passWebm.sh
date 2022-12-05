#! /bin/bash

echo "Running first pass..."
ffmpeg -i "$1" -c:v libvpx -threads 8 -quality good -cpu-used 0 -lag-in-frames 16 \
 -auto-alt-ref 1 -qcomp 1 -b:v 1M -an -sn -y -f webm -pass 1 /dev/null

echo "Running second pass..."
ffmpeg -i "$1" -c:v libvpx -threads 8 -quality good -cpu-used 0 -lag-in-frames 16 \
 -auto-alt-ref 1 -qcomp 1 -b:v 1M -an -sn -y -f webm -pass 2 "$1".webm
