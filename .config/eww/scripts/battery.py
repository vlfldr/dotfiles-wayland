import os
import sys

# to get battery name, look at output of `upower --dump`
batName = 'battery_BAT1'

dischargingGlyphs = [
   '',
   '',
   '',
   '',
   '',
   '',
   '',
   '',
   '',
   ''
]

chargingGlyphs = [
   '' ,
   '' ,
   '' ,
   '' ,
   '' ,
   '' ,
   '' 
]

def getGlyph(p, batState):
    if batState == 'discharging':
        return dischargingGlyphs[ int( int(p[:-1]) // 10 ) - 1 ]
    else:
        lvl = int(int(p[:-1]))
        if lvl < 20:
            res = chargingGlyphs[0]
        elif lvl < 30:
            res = chargingGlyphs[1]
        elif lvl < 40:
            res = chargingGlyphs[2]
        elif lvl < 50:
            res = chargingGlyphs[3]
        elif lvl < 65:
            res = chargingGlyphs[4]
        elif lvl < 80:
            res = chargingGlyphs[5]
        elif lvl < 90:
            res = chargingGlyphs[6]
        else:
            res = chargingGlyphs[6]

        return res

raw = os.popen('upower --dump').read()

raw = raw[ raw.find(batName): ]
raw = raw[ :raw.find('Device') ]

batState = raw[ raw.find('state'): ]
batState = batState[ 6:batState.find('\n') ].strip()

batLevel = raw[ raw.find('percentage'): ]
batLevel = batLevel[ 11:batLevel.find('\n') ].strip()

timeIdx = raw.find('time to empty')
suffix = ' remaining'
if timeIdx == -1:
    timeIdx = raw.find('time to full:')
    suffix = ' until full'
batTime = raw[ timeIdx: ]
batTime = batTime[ 14:batTime.find('\n') ].strip()

if batTime == '':
    batTime = raw[ raw.find('time to full'): ]
    batTime = batTime[ 13:batTime.find('\n') ].strip()

#print(batState)
#print(batTime)

if len(sys.argv) > 1 and sys.argv[1] == 'time':
    print(f'{batLevel} - {batTime}{suffix}', flush=True)
    sys.exit(0)

print( getGlyph(batLevel, batState), flush=True)
