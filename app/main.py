import time
import os
import json
from config import outputFile, codes, stopFind, commands, allCommands, zapretPath, zapretProcess, backupPath, CONTEXT_FILE
from app.public.wright import wright
from app.TextAI import requestTextAI
from app.customCommands.saveBackup import saveBackup
from app.customCommands.clearFile import clearFile

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

def main(queue,outputText,commandToSound):
    while True:
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
            if firstWord in allCommands:
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
                    wright('Restarting zapret program...')
                    # Kill existing process if running
                    os.system(f'taskkill /F /IM {os.path.basename(zapretProcess)}')
                    # Start new instance
                    os.startfile(zapretPath)

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
            else:
                response = requestTextAI(res)
                outputText.put(response)
                wright(response)

            wright('------------')