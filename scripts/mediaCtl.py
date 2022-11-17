import os
import sys

# path to album art (updated by aart.sh)
imgPath = '/tmp/aart'

# send dunst notification

if not os.path.exists(imgPath):
    imgPath = ''

nowPlaying = os.popen('mpc').read().split('\n')[0].strip()

os.system(f'dunstify \'{nowPlaying}\'')
