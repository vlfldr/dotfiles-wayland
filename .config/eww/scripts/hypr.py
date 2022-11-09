import socket
import os
import time

# workspace config
workspaces = {
    1: ['', 'active'],
    2: ['', 'active'],
    3: ['', 'inactive'],
    4: ['', 'inactive'],
    5: ['♫', 'inactive'],
    6: ['◇', 'inactive'],
}

def getWorkspaceStatus(curWorkspaceID):
    for ws in workspaces:
        workspaces[ws][1] = 'inactive'

    # read from hyperctl. must wait a couple ms for accurate workspace data
    time.sleep(.015)
    for ws in os.popen('hyprctl workspaces').read().split('workspace ID ')[1:7]:
        workspaces[ int(ws[0]) ][1] = 'active' 
        print(ws)
    # construct widget string
    widgetStr = '(box :class \"hyprland container\" :valign \"center\" :halign \"start\" :spacing 5 '

    for ws in workspaces:
        wsLabel, wsClass = workspaces[ws][0], workspaces[ws][1]
        if ws == int(curWorkspaceID):
            wsClass = 'current'
        widgetStr += f" (button :onclick \"hyprctl dispatch workspace {ws} \" :class \"{wsClass}\" \"{wsLabel}\")"

    widgetStr += ')'

    return widgetStr

# initialization
print( getWorkspaceStatus("1"), flush=True)

# get hyprland socket ID
hid = os.environ['HYPRLAND_INSTANCE_SIGNATURE']

# listen for events
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect('/tmp/hypr/' + hid + '/.socket2.sock')

    while True:

        rawData = str( client.recv(1024), 'UTF-8' )
        events = rawData.split('\n')
        
        for e in events:
            es = e.split('>>')
            if es == ['']:
                continue
            eType, eData = es[0], es[1]
        
            # workspace change
            if eType == 'workspace':
                widgetStr = getWorkspaceStatus( eData )

                # output widget literal for eww listener
                print(widgetStr, flush=True)

            elif eType in ('activewindow', 'createworkspace', 'destroyworkspace'):
                continue
            else:
                print('Unhandled type: ' + eType + ' :: ' + eData)
