import os
import sys

glyph = '?'
upGlyph = ''

status = os.popen("nmcli d | grep 'wifi ' | awk '{print $3}'").read().strip()

if status == 'connected':
    glyph = upGlyph

print(glyph, flush=True)
