import os
import logging
import datetime
import subprocess
import json

# CONFIGURATION ###
borgRepo = 'ssh://steve@192.168.1.5:777/green/daily-backups/framework'
logFile = '/home/steve/.config/borg/borg.log'

os.environ['BORG_REPO'] = borgRepo
os.environ['BORG_PASSPHRASE'] = 'FalseDonkeyFuelCellStapler!'

excludeDirs = [
    'home/*/.cache/*',
    'var/tmp/*',
    'media',
    'run/media',
    'sys/*',
    'dev/*',
    'proc/*',
    'mnt/*',
    'tmp/*',
    'run/*',
    'lost+found/*',
    'pagefile.sys',
    'hiberfile.sys',
    '*/system.journal',
    'home/*/.cargo',
    'home/steve/backups',
    'home/steve/music',
    'home/steve/gold',
    'home/steve/sync',
    'home/steve/.rustup',
    'root/.config/borg/security/*',
    'home/*/.mozilla/firefox/*/Cache',
    '*.Trash-1000'
]

retentionSettings = {
    '--keep-daily':   7,
    '--keep-weekly':  4,
    '--keep-monthly': 12
}

# END CONFIGURATION ###

# total size of disk in GB. used to calc % progress
#totalSize = int(os.popen('du -msh / 2>/dev/null').read()[:-2].replace('G', '').strip())


logging.basicConfig(filename=logFile,
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)s :: %(message)s',
                    datefmt='%m-%d-%Y %-I:%M:%S %p')

os.system("sudo -u steve dunstify 'Backup Started '")
logging.info('--- BACKUP STARTED ---')
logging.info('Building borg command...')

borgCmd = ['borg', 'create', '--compression', 'lz4', '--exclude-caches',
           '--stats', '--json', '--show-rc', '--progress']

# add exlude directories
for d in excludeDirs:
    borgCmd += ['--exclude', d]

fmtDt = datetime.datetime.now().strftime('%m-%d-%y_%I.%M.%S%p')
borgCmd += [f'::{fmtDt}', '/']

logging.info('Executing backup with command:')
logging.info(borgCmd)


# communicate() prints live progress from script for status bar
logging.info('Backup in progress...')
res = subprocess.Popen(borgCmd, stdout=subprocess.PIPE).communicate()

# extract info from stats (returned in JSON)
resStr = res[0].decode('utf-8')
resJSON = json.loads(resStr)

timeSeconds = str(resJSON['archive']['duration'])[:-7]
stats = resJSON['archive']['stats']

numFiles = stats['nfiles']
oSize = stats['original_size']
cSize = stats['compressed_size']
dSize = stats['deduplicated_size']

logging.info('Archive created! Time elapsed: ' + timeSeconds + ' seconds')
logging.info(f"Number of files in archive: {numFiles}")
logging.info(f"Original size: {oSize}B")
logging.info(f"Compressed size: {cSize}B")
logging.info(f"Deduplicated size: {dSize}B")

# borg prune
pruneCmd = 'borg prune'
for rule in retentionSettings:
    pruneCmd += f' {rule} {retentionSettings[rule]}'
logging.info('Executing prune with command:')
logging.info(pruneCmd)
os.system(pruneCmd)

# borg compact
logging.info('Executing compact with command: borg compact')
os.system('borg compact')

os.system("sudo -u steve dunstify 'Backup Complete '")
logging.info('--- BACKUP COMPLETE ---')
