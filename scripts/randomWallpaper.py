import os
import random
import time

wpDir = '/home/steve/wallpapers'
tMins = 15

os.system('swww init')
time.sleep(.25)

while True:
    randImg = os.path.join(wpDir, random.choice(os.listdir(wpDir)))
    
    os.system(f'swww img {randImg}')

    time.sleep( tMins * 60 )
