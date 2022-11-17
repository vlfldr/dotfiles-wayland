import time
import os

time.sleep(10)

os.system('sshfs steve@192.168.1.5:/green/music /home/steve/music -p 777')
