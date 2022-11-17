import os
import sys

# depends on `light`
# usage: python dunstBrightness.py <up/down>

# exit upon improper arguments
if len(sys.argv) < 2:
    sys.exit(0)

# decrease = -U
op = '-U'

# increase = -A
if sys.argv[1] == 'up':
    op = '-A'

# modify brightness
os.system(f'light {op} 10')

# send dunst notification
os.system('eww update showBrightness=true')
os.system('eww update closeBrightnessTimer=2')