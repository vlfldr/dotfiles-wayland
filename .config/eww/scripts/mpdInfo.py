import os
import sys

raw = os.popen("mpc").read().split('\n')

nowPlaying = raw[0]
progress = raw[1]

if "[playing]" in progress:
    os.system('eww update playIcon=')
else:
    os.system('eww update playIcon=')

if len(nowPlaying) > 51:
    nowPlaying = nowPlaying[:51] + '...'
    os.system('eww update musicPosition=10')
else:
    leftMargin = 140 - (len(nowPlaying) * 1.2)
    os.system('eww update musicPosition=' + str(leftMargin))

intProgress = progress[progress.find(' (') + 2:-2]

if nowPlaying[:7] == 'volume:':
    os.system('eww update showMPD=false')
    sys.exit(0)

if "[playing]" in progress or "[paused]" in progress:
    os.system('eww update showMPD=true')
    os.system('eww update mpdProgress=' + intProgress)


print(nowPlaying, flush=True)
