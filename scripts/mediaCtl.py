import os
import sys
import time

if len(sys.argv) < 2:
    sys.exit(0)

cmd = sys.argv[1]

res = os.popen('mpc ' + cmd).read()
lines = res.split()

if '[playing]' in res:
    time.sleep(0.2)     # wait for song info to update
    os.system('eww update showNowPlaying=true')
    time.sleep(3)
    os.system('eww update showNowPlaying=false')
