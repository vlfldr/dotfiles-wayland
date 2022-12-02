import os
import time

time.sleep(5)
os.system('hyprctl keyword windowrule \"workspace unset,cava\"')
os.system('hyprctl keyword windowrule \"workspace unset,ncmpcpp\"')
os.system('hyprctl keyword windowrule \"workspace unset,Sxiv\"')
os.system('hyprctl keyword windowrule \"size unset,cava\"')
os.system('hyprctl keyword windowrule \"move unset,cava\"')
os.system('hyprctl keyword windowrule \"move unset,ncmpcpp\"')
os.system('hyprctl keyword windowrule \"size unset,ncmpcpp\"')
