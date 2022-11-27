import os
import sys
import subprocess
import time

# TODO: figure out autoconnect
# TODO: separate color/icon for remembered, currently paired

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
    os.system('bluetoothctl power ' + subCmd + ' && bluetoothctl agent ' + subCmd + ' && bluetoothctl discoverable ' + subCmd + ' && bluetoothctl --timeout 45 scan on')

if cmd == 'scan':
    devices = []
    raw = os.popen('bluetoothctl devices').read().split('\n')

    if raw == []:
        print('', flush=True)
        sys.exit(0)

    connected = os.popen('bluetoothctl devices Connected').read()
    trusted = os.popen('bluetoothctl devices Trusted').read()

    for d in raw:
        if len(d) < 25:
            continue
        devices += [ {'addr': d[7:24], 'name': d[25:]} ]

    ewwStr = "(box :class \"device-list\" :orientation \"v\" " 

    for d in devices[::-1]:
        dClass = "device"
        dIcon = ""
        if d['addr'] in connected:
            dClass += " device-connected"
            dIcon = ""
        elif d['addr'] in trusted:
            dClass += " device-trusted"
            dIcon = ""
        ewwStr += "(box :space-evenly false :class \"" + dClass + "\" (button :onclick \"python scripts/bt.py connect " \
            + d['addr'] + "\" \"" + d['name'] + "\") (button :class \"device-icon\" \"" + dIcon + "\")) "
        
    ewwStr += ")"
    print(ewwStr, flush=True    )

if cmd == 'connect' and len(sys.argv) == 3:
    addr = sys.argv[2]
    os.system('bluetoothctl trust ' + addr)
    os.system('bluetoothctl connect ' + addr)

if cmd == 'disconnect' and len(sys.argv) == 3:
    os.system('bluetoothctl disconnect ' + sys.argv[2])
 
