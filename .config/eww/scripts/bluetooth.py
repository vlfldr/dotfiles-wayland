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
    
if cmd == 'scan':
    proc = subprocess.Popen(['unbuffer', 'bluetoothctl', 'scan', 'on'], bufsize=0, stdout=subprocess.PIPE)
    for line in iter(proc.stdout.readline, b''):
        print(line.decode('utf-8')[:-1]) # [:-1] to cut off newline char
    proc.stdout.close()
    proc.wait()