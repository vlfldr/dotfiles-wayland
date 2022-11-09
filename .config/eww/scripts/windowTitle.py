import os
import socket

# window replacement rules
# <search_text>: <replace_with>
replacementRules = {
    ' — Firefox Nightly': '',
}

def applyRules(winTitle):
    for r in replacementRules:
        if r in winTitle:
            return winTitle.replace(r, replacementRules[r])

    return winTitle

# get hyprland socket ID
hid = os.environ['HYPRLAND_INSTANCE_SIGNATURE']

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
        
            # focused window change
            if eType == 'activewindow':
                if eData == ',':
                    print('', flush=True)
                    continue

                spl = eData.split(',')
                winClass, winTitle = spl[0], applyRules(spl[1])
                
                print(winTitle, flush=True)

            elif eType in ('workspace', 'createworkspace', 'destroyworkspace'):
                continue
            else:
                print('Unhandled type: ' + eType + ' :: ' + eData)

