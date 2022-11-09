import os
import sys

log = '/home/steve/.config/borg/borg.log'

if not os.path.exists(log):
    sys.exit(0)

# get last line
with open(log, 'rb') as f:
    try:  # catch OSError in case of a one line file
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
    except OSError:
        f.seek(0)
    last_line = f.readline().decode()

# print(last_line)

if 'BACKUP COMPLETE' not in last_line:
    print(' ', flush=True)
