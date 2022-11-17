import os
import sys

raw = os.popen("mpc").read().split('\n')

nowPlaying = raw[0]
progress = raw[1]

if len(nowPlaying) > 40:
    nowPlaying = nowPlaying[:40] + '...'

intProgress = progress[progress.find(' (') + 2:-2]

if nowPlaying[:7] == 'volume:':
    os.system('eww update showMPD=false')
    sys.exit(0)

if "[playing]" in progress or "[paused]" in progress:
    os.system('eww update showMPD=true')
    os.system('eww update mpdProgress=' + intProgress)

if "[playing]" in progress:
    os.system('eww update playIcon=')
else:
    os.system('eww update playIcon=')

print(nowPlaying, flush=True)
