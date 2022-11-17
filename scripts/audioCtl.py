import os
import sys

if len(sys.argv) < 2 or sys.argv[1] not in ['up', 'down', 'mute']:
    sys.exit(0)

isMuted = False

if sys.argv[1] == 'down':
    os.system('pactl set-sink-mute @DEFAULT_SINK@ false')
    os.system('pactl set-sink-volume @DEFAULT_SINK@ -5%')
elif sys.argv[1] == 'up':
    os.system('pactl set-sink-mute @DEFAULT_SINK@ false')
    os.system('pactl set-sink-volume @DEFAULT_SINK@ +5%')
else:
    isMuted = 'yes' in os.popen('pactl get-sink-mute @DEFAULT_SINK@').read()
    os.system('pactl set-sink-mute @DEFAULT_SINK@ ' + str(not isMuted).lower())

# show eww volume bar
os.system('eww update showVolume=true')
os.system('eww update closeVolumeTimer=2')
