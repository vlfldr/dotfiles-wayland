import os
import sys

raw = os.popen("nmcli dev wifi list | awk '/\*/{if (NR!=1) {print $all}}'").read()[1:].strip()

ff = []    # formatted fields
fields = raw.split('  ')
for f in fields:
    f = f.strip()
    if f != '': 
        ff.append(f)

print(f"""Connected to: {ff[1]}
Signal strength: {ff[5]}%
Link speed: {ff[4]}
MAC Address: {ff[0]}""", flush=True)

