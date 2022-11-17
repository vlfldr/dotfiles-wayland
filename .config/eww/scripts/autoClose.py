import sys
import os

if len(sys.argv) < 2:
    sys.exit(0)

cmd = sys.argv[1][0].upper() +  sys.argv[1][1:]

isOpen = int(os.popen(f'eww get close{cmd}Timer').read())

if isOpen != 0:
    isOpen -= 1
    os.system(f'eww update close{cmd}Timer={isOpen}')

    if isOpen == 0:
        os.system(f'eww update show{cmd}=false')
    