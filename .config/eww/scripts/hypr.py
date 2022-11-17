import socket
import os

# hypr.py - to be run constantly in background
# connects to hyprland socket, updates eww vars based on received events
# github.com/vlfldr

# window title replacement rules
replacementRules = {
    ' — Firefox Nightly': '',
}


def applyRules(winTitle):
    for r in replacementRules:
        winTitle = winTitle.replace(r, replacementRules[r])

    return winTitle


# hyprland socket ID
hid = os.environ['HYPRLAND_INSTANCE_SIGNATURE']

# last active workspace
prevActive = "1"

# listen for events
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
    client.connect('/tmp/hypr/' + hid + '/.socket2.sock')

    while True:
        rawData = str(client.recv(1024), 'UTF-8')
        events = rawData.split('\n')

        for e in events:
            es = e.split('>>')
            if es == [''] or len(es) == 1:
                continue

            eType, eData = es[0], es[1].strip()

            # workspace change
            if eType == 'workspace':
                os.system(f'eww update ws{eData}=ws_current')
                os.system(f'eww update ws{prevActive}=ws_active')

                prevActive = eData

            # window focus change
            elif eType == 'activewindow':
                # empty workspace
                if eData == ',':
                    os.system('eww update winvar=\"\"')
                    continue

                spl = eData.split(',')
                if len(spl) == 1:
                    continue

                winClass, winTitle = spl[0], applyRules(spl[1]) # apply rules
                winTitle = winTitle.replace("`", "")    # sanitize
                if len(winTitle) > 86:
                    winTitle = winTitle[:86] + '...'    # max length
                
                os.system(f'eww update winvar=\"{winTitle}\"')

            # on new workspace created (handled in workspace change)
            elif eType == 'createworkspace':
                print()
            
            # on switch away from empty workspace
            elif eType == 'destroyworkspace':
                os.system(f'eww update ws{eData}=ws_inactive')

            elif eType in ['openwindow', 'closewindow', 'openlayer', 'closelayer']:
                continue

            else:
                print('Unhandled type: ' + eType + ' :: ' + eData)
