import os
import sys
import subprocess

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
    os.system('bluetoothctl power ' + subCmd)

    # scan for 10 seconds when BT turned on
    if subCmd == 'on':
        time.sleep(2)
        os.system('bluetoothctl scan on')
        time.sleep(10)
        os.system('bluetoothctl scan off')

if cmd == 'list':
    ewwStr = "(box :orientation 'v' "

    devs = os.popen('bluetoothctl devices').read()
    print(devs)
    
    