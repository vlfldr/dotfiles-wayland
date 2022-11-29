import os
import sys

if len(sys.argv) < 2 or sys.argv[1] not in ['up', 'down', 'mute']:
    sys.exit(0)

isMuted = False
curVol = int(os.popen("pactl get-sink-volume @DEFAULT_SINK@ | awk '{print $5}' | tr -d '%'").read().strip())

if sys.argv[1] == 'down':
    os.system('pactl set-sink-mute @DEFAULT_SINK@ false')
    os.system('pactl set-sink-volume @DEFAULT_SINK@ -5%')
    os.system('eww update isMuted=no')
    curVol -= 5;
elif sys.argv[1] == 'up' and curVol < 95:
    os.system('pactl set-sink-mute @DEFAULT_SINK@ false')
    os.system('pactl set-sink-volume @DEFAULT_SINK@ +5%')
    curVol += 5;
elif sys.argv[1] == 'up':
    os.system('eww update isMuted=no')
elif sys.argv[1] == 'mute':
    isMuted = 'yes' in os.popen('pactl get-sink-mute @DEFAULT_SINK@').read()
    muteStr = 'no'
    if isMuted:
        muteStr = 'yes'
    os.system('eww update isMuted=' + muteStr)
    os.system('pactl set-sink-mute @DEFAULT_SINK@ ' + str(not isMuted).lower())

os.system('eww update curVolume=' + str(curVol))
# show eww volume bar
os.system('eww update showVolume=true')
os.system('eww update closeVolumeTimer=2')
