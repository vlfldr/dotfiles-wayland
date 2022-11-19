import os
import sys
import re

lastNowPlaying = ''

# wait for event
while True:
    ev = os.popen('mpc idle').read().strip()

    # when event recieved, get song info
    if ev == 'player':
        raw = os.popen('mpc').read().split('\n')
        nowPlaying = raw[0]
        if len(raw) > 1:
            status = raw[1]

        # yields array [ playing/paused/stopped, #X/Y, MM:SS/MM:SS, (<progress>%) ]
        if status != '':
            status = re.split(r"\s{1,}", status)
        else:
            continue

        # play, next, prev
        if status[0] == '[playing]' and nowPlaying != lastNowPlaying:
            continue

        # seek
        elif status[0] == '[playing]':
            continue

        # pause
        elif status[0] == '[paused]':
            continue

        lastNowPlaying = nowPlaying
        
