import os
import sys

cmd = sys.argv[1]

if cmd == 'toggle':
    status = os.popen('bluetoothctl show | grep Powered').read()

    subCmd = 'off'
    if 'no' in status:
        subCmd = 'on'

    os.system('bluetoothctl power ' + subCmd)
    os.system('eww update btEnabled=false')
