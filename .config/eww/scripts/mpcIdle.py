import os
import sys
import re
import json

def ewwUpd(ewwVar, newVal):
    newVal = str(newVal)
    os.system(f'eww update {ewwVar}=\"{newVal}\"')

# wait for event
while True:
    ev = os.popen("mpc idle").read().strip()

    # on event recieved
    if ev == 'player':
        # get now playing & player status info
        raw = os.popen('mpc --format %artist%\\\\n%title%\\\\n%album%\\\\n%file%').read().split('\n')

        # stop
        if raw[0][:7] == 'volume:':
            ewwUpd('showMpd', 'false')
            ewwUpd('mpdPlaying', 'false')
            continue
        
        songInfo = {"artist": raw[0], "title": raw[1], "album": raw[2],
        "format": raw[3][::-1][:raw[3][::-1].find('.')][::-1].upper() }

        # yields array [ playing/paused/stopped, #X/Y, MM:SS/MM:SS, (<progress>%) ]
        if raw[4] != '':
            status = re.split(r"\s{1,}", raw[4])
        else:
            continue

        if len(status) != 4:
            os.system('dunstify \"mpcIdle has crashed - invalid status array!\"')
            sys.exit(0)

        # hacky way to center between elements (adjust margins)
        if len(songInfo['artist']  + ' - ' + songInfo['title'] ) > 51:
            songInfo['title']  = songInfo['title'] [:48 - len(songInfo['artist'] )] + '...'
            os.system('eww update musicPosition=10')
        else:
            leftMargin = 140 - (len(songInfo['artist']  + ' - ' + songInfo['title'] ) * 1.2)
            os.system('eww update musicPosition=' + str(leftMargin))

        # next, prev, play, pause, seek
        if status[0] == '[playing]':
            ewwUpd('songInfo', json.dumps(songInfo).replace('"', '\\"'))
            ewwUpd('showMpd', 'true')
            ewwUpd('mpdPlaying', 'true')
            ewwUpd('showNowPlaying', 'true')
            ewwUpd('closeNowPlayingTimer', 4)
            ewwUpd('mpdProgress', status[3][1:-2])  # TODO: this is only updated on events

        # pause
        elif status[0] == '[paused]':
            ewwUpd('mpdPlaying', 'false')        
