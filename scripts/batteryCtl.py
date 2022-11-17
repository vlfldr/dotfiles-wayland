import psutil
import time
import os

firstWarn = [25, False]
secondWarn = [10, False]

while True:
    bat = psutil.sensors_battery()
    if not bat.power_plugged:
        if bat.percent <= firstWarn[0] and firstWarn[1] == False:
            os.system("dunstify ' Battery Low' -r 003")
            firstWarn[1] = True
        
        if bat.percent <= secondWarn[0] and secondWarn[1] == False:
            os.system("dunstify ' Battery Critical' -r 003")
            secondWarn[1] = True
    else:
        firstWarn[1], secondWarn[1] = False, False
    
    time.sleep(15)
