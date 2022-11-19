import os
import sys

raw =  os.popen('hyprctl workspaces').read()

scratchpadActive = 'workspace ID -99' in raw

if scratchpadActive:
    ws = os.popen('hyprctl activewindow').read()
    idx = ws.find('workspace: ') + 11
    ws = ws[idx:idx+1]
    
    os.system('hyprctl dispatch togglespecialworkspace 0')
    os.system('hyprctl dispatch movetoworkspace ' + ws)

else:
    os.system('hyprctl dispatch movetoworkspacesilent special')
