import time
import os
import json
from config import allCommands
from app.utils.wright import wright
from app.TextAI import requestTextAI
from app.customCommands.saveBackup import saveBackup
from app.customCommands.clearFile import clearFile
from app.customCommands.show_branches import show_branches
from app.customCommands.whatYouCan import text_commands_help, voice_commands_help
from app.customCommands.timer import timer
from app.utils.content import load_context, save_context

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    outputFile = devolp_config['outputFile']
    codes = devolp_config['codes']
    stopFind = devolp_config['stopFind']
    commands = devolp_config['commands']
    CONTEXT_FILE  = devolp_config['CONTEXT_FILE']

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    useZapret = config['useZapret']
    zapretPath = config['zapretPath']
    zapretProcess = config['zapretProcess']
    wakeWord = config['wakeWord']

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

def is_command(phrase, commands):
    
    if phrase.split()[0].lower() in wakeWord:
        phrase = ' '.join(phrase.split()[1:])
    # print(phrase, phrase.split()[0], wakeWord)
    if phrase in commands:
        return phrase, None
    for cmd in commands:
        if phrase.startswith(cmd):
            return cmd, phrase.split(cmd,1)[1]
    
def main(queue,outputText,commandToSound,condition):
    current_branch = "default"
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

            command = None
            argument = None

            for cmd_group in commands.values():
                try:
                    command, argument = is_command(res, cmd_group)
                    break
                except:
                    pass
            # print(command, argument)
            # can be command
            if command:

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
                    context_file = f"promts/{current_branch}/context.json"
                    with open(context_file, 'w', encoding='utf-8') as f:
                        json.dump([], f)
                    wright(f"Контекст для ветки '{current_branch}' очищен.")

                elif command in commands['exitCommands']:
                    condition.set()

                elif command in commands['branchCommands']:
                    show_branches()

                elif command in commands['helpCommands']:
                    text_help = text_commands_help()
                    outputText.put(text_help)
                
                elif command in commands['aboutCommands']:
                    voice_help = voice_commands_help()
                    outputText.put(voice_help)

                elif command in commands['selectBranchCommands']:
                    print(argument)

                    if argument:
                        current_branch = argument
                        wright(f"Текущая ветка изменена на: {current_branch}")
                    else:
                        wright("Ошибка: укажите имя ветки для переключения.")
                
                # elif command in commands['timerCCommands']:
                #     timer()
            else:
                pass
                response = requestTextAI(res, current_branch)
                outputText.put(response)
                wright(response)

            wright('------------')