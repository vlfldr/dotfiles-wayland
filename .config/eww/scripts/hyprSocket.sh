#! /bin/bash

function handle {
    if [[ ${1:0:9} == "workspace" ]]; then
        echo "${1}"
    fi

    if [[ ${1:0:12} == "activewindow" ]]; then
        winTitle=$("${1}" | cut -d, -f2-)
        eww update winvar="$winTitle"
    fi
    
}

socat - UNIX-CONNECT:/tmp/hypr/$(echo $HYPRLAND_INSTANCE_SIGNATURE)/.socket2.sock | while read -r line; do handle "$line"; done
