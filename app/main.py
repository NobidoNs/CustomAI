import time
import os
import json
import threading
from config import allCommands
from app.utils.wright import wright
from app.TextAI import requestTextAI
from app.customCommands.saveBackup import saveBackup
from app.customCommands.clearFile import clearFile
from app.customCommands.show_branches import show_branches
from app.customCommands.whatYouCan import text_commands_help, voice_commands_help
from app.customCommands.timer import timer
from app.utils.content import load_context, save_context
from app.customAI.timeAI import convertTime

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    outputFile = devolp_config['outputFile']
    codes = devolp_config['codes']
    stopFind = devolp_config['stopFind']
    commands = devolp_config['commands']

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

def parse_command(phrase, commands):
    
    if phrase.split()[0].lower() in wakeWord or phrase.split()[0].lower() == 'чарльз':
        phrase = ' '.join(phrase.split()[1:]).lower()
    # print(phrase, phrase.split()[0], wakeWord)
    if phrase in commands:
        return phrase, None
    for cmd in commands:
        if phrase.startswith(cmd):
            # print(cmd, phrase[len(cmd):].strip())
            return cmd, phrase[len(cmd):].strip()
    
def main(queue,outputText,commandToSound,condition):
    current_branch = "default"
    active_timer = None
    timer_stop_event = threading.Event()
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
                    command, argument = parse_command(res, cmd_group)
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
                
                elif command in commands['setTimerCommands']:
                    if argument:
                        timer_seconds = convertTime(argument)
                        if timer_seconds == 0:
                            wright("Не удалось преобразовать время в секунды.")
                            continue
                        if active_timer:
                            timer_stop_event.set()
                            active_timer.join() 
                        timer_stop_event.clear()
                        wright(f"Таймер установлен на {timer_seconds} секунд.")
                        active_timer = threading.Thread(target=timer, args=(timer_seconds, timer_stop_event), daemon=True)
                        active_timer.start()
                    else:
                        wright("Ошибка: укажите время для таймера.")

                elif command in commands['stopTimerCommands']:
                    if active_timer: 
                        timer_stop_event.set() 
                        active_timer.join()
                        wright("Таймер остановлен.")
                    else:
                        wright("Таймер не запущен.")
            else:
                pass
                response = requestTextAI(res, current_branch)
                outputText.put(response)
                wright(response)

            wright('------------')
    if active_timer:
        timer_stop_event.set()
        active_timer.join()