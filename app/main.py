import time
import os
import json
from config import allCommands
from app.utils.wright import wright
from app.TextAI import requestTextAI
from app.customCommands.saveBackup import saveBackup
from app.customCommands.clearFile import clearFile
from app.customCommands.show_backups import show_backups
from app.customCommands.whatYouCan import text_commands_help, voice_commands_help
from app.customCommands.timer import timer

with open('devolp_config.json', 'r') as file:
    devolp_config = json.load(file)
    outputFile = devolp_config['outputFile']
    codes = devolp_config['codes']
    stopFind = devolp_config['stopFind']
    commands = devolp_config['commands']
    CONTEXT_FILE  = devolp_config['CONTEXT_FILE']

with open('config.json', 'r') as file:
    config = json.load(file)
    useZapret = config['useZapret']
    zapretPath = config['zapretPath']
    zapretProcess = config['zapretProcess']

def requestInFile():
    with open(outputFile, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()

    for indexLine in range(1,len(lines)+1):
        line = lines[-indexLine]
        for code in codes:
            if code in line:
                return "".join(lines[-indexLine:]).split(code,1)[1]
        if line in stopFind:
            return ''
    return ''

def main(queue,outputText,commandToSound,condition):
    while not condition.is_set():
        # await queue
        req = requestInFile()
        if queue.empty() and not req:
            time.sleep(1)
        else:
            if req: 
                res = req
            else:
                res = queue.get()
                wright(res)

            # can be command
            try:
                firstWord = res.split(' ', 1)[0]
                for i in commands:
                    if res in i:
                        firstWord = i
            except:
                firstWord = None

            # command check
            if firstWord in allCommands or res in allCommands:
                command = firstWord
                argument = res.split(' ', 1)[1] if ' ' in res else None

                # command logic
                if command in commands['muteCommands']:
                    wright('stop')
                    commandToSound.put('stop')

                elif command in commands['voiceCommands']:
                    wright('MUTE')
                    commandToSound.put('-mute')

                elif command in commands['clearCommands']:
                    clearFile()
                    continue

                elif command in commands['restartZapretCommands']:
                    if useZapret:
                        try:
                            wright('Restarting zapret program...')
                            # Kill existing process if running
                            os.system(f'taskkill /F /IM {os.path.basename(zapretProcess)}')
                            # Start new instance
                            os.startfile(zapretPath)
                        except:
                            wright('Failed to restart zapret program')
                    else:
                        wright('Zapret is not enabled in config.json')

                elif command in commands['saveCommands']:
                    backup_file = saveBackup(argument)
                    wright(f'Backup saved as: {backup_file}')

                elif command in commands['setSpeedCommands']:
                    commandToSound.put(f'-speed {argument}')

                elif command in commands['upSpeedCommands']:
                    commandToSound.put(f'-speed up')
                elif command in commands['downSpeedCommands']:
                    commandToSound.put(f'-speed down')
                
                elif command in commands['clearContextCommands']:
                    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
                        json.dump([], f)
                    wright('Context cleared')

                elif command in commands['exitCommands']:
                    condition.set()

                elif command in commands['branchCommands']:
                    show_backups()

                elif command in commands['helpCommands']:
                    text_help = text_commands_help()
                    outputText.put(text_help)
                
                elif command in commands['aboutCommands']:
                    voice_help = voice_commands_help()
                    outputText.put(voice_help)
                
                # elif command in commands['timerCCommands']:
                #     timer()
            else:
                response = requestTextAI(res)
                outputText.put(response)
                wright(response)

            wright('------------')