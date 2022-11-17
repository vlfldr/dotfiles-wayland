import os
import time

os.system('fusermount3 -u /home/steve/music')   # unmount SSHFS
os.system('eww kill')                           # kill status bar
time.sleep(.1)
os.system('hyprctl dispatch exit 0')
