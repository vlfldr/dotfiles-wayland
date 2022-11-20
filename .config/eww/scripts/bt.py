import os
import sys
import subprocess
import time

cmd = sys.argv[1]

status = os.popen('bluetoothctl show | grep Powered').read()

if cmd == 'status':
    ewwCmd = "true"
    if ': no' in status:
        ewwCmd = "false"
    os.system('eww update btEnabled=' + ewwCmd)

if cmd == 'toggle':
    ewwCmd, subCmd = "false", "off"
    if ': no' in status:
        ewwCmd, subCmd = "true", "on"
    os.system('eww update btEnabled=' + ewwCmd)
    # will not scan if turned off
    os.system('bluetoothctl power ' + subCmd + ' && sleep 2 && bluetoothctl --timeout 45 scan on')

if cmd == 'scan':
    devices = []
    raw = os.popen('bluetoothctl devices').read().split('\n')
    if raw == []:
        print('', flush=True)
        sys.exit(0)

    for d in raw:
        d = d.split(' ')
        if len(d) != 3:
            continue
        devices += [ {'name': d[2], 'addr': d[1]} ]

    ewwStr = "(eventbox (box :class \"device-list\" :orientation \"v\" " #:spacing \"10\""

    for d in devices:
        ewwStr += "(box :class \"device\" (button :onclick \"bluetoothctl connect " + d['addr'] + "\" \"" + d['name'] + "\")) "
        
    ewwStr += "))"
    print(ewwStr, flush=True    )
    
    