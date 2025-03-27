import time
import os
import json
import threading
from app.config import allCommands
from app.utils.wright import wright
from app.TextAI import requestTextAI
from app.customCommands.saveBackup import saveBackup
from app.customCommands.clearFile import clearFile
from app.customCommands.show_branches import show_branches
from app.customCommands.whatYouCan import text_commands_help, voice_commands_help
from app.customCommands.timer import timer
from app.customAI.timeAI import convertTime
from app.customCommands.restoreChat import restore_chat
from app.customCommands.showChats import showChats
from app.customCommands.selectChat import selectChat
from app.sysControl.run import runPrograms

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    outputFile = devolp_config['outputFile']
    codes = devolp_config['codes']
    stopFind = devolp_config['stopFind']
    commands = devolp_config['commands']
    scriptsNames = devolp_config['scripts']
    voices = devolp_config['voices']

with open('config.json', 'r+', encoding='utf-8') as file:
    config = json.load(file)
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

def parse_command(phrase, command):
    jarv = phrase.split()[0].lower()
    if jarv in wakeWord or jarv == 'чарльз' or jarv == 'джар':
        phrase = ' '.join(phrase.split()[1:]).lower()
    # print(phrase, command)

    if phrase.startswith(command):
        # print(command, phrase[len(command):].strip())
        return command, phrase[len(command):].strip()
    
def main(queue,outputText,commandToSound,condition):
    current_branch = "джарвис"
    chat = "context"
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

            for cmd_group in allCommands:
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

                elif command in commands['disableTTS']:
                    wright('MUTE', log=True)
                    commandToSound.put('-mute')

                elif command in commands['clearCliCommands']:
                    clearFile()
                    continue

                elif command in commands['backupCommands']:
                    backup_file = saveBackup(argument)
                    wright(f'Backup saved as: {backup_file}', log=True)

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
                    wright(f"Контекст для ветки '{current_branch}' очищен.", say=outputText)

                elif command in commands['exitCommands']:
                    condition.set()

                elif command in commands['helpCommands']:
                    text_help = text_commands_help()
                    outputText.put(text_help)
                
                elif command in commands['aboutCommands']:
                    wright(voice_commands_help(), say=outputText)
                    
                
                # Таймер
                elif command in commands['setTimerCommands']:
                    if argument:
                        timer_seconds = convertTime(argument)
                        if timer_seconds == 0:
                            wright("Не удалось преобразовать время в секунды.", say=outputText)
                            continue
                        if active_timer:
                            timer_stop_event.set()
                            active_timer.join() 
                        timer_stop_event.clear()
                        wright(f"Таймер установлен на {timer_seconds} секунд.", say=outputText)
                        active_timer = threading.Thread(target=timer, args=(timer_seconds, timer_stop_event), daemon=True)
                        active_timer.start()
                    else:
                        wright("Ошибка: укажите время для таймера.", say=outputText)

                elif command in commands['stopTimerCommands']:
                    if active_timer: 
                        timer_stop_event.set() 
                        active_timer.join()
                        wright("Таймер остановлен.", say=outputText)
                    else:
                        wright("Таймер не запущен.", say=outputText)
                
                # Чаты
                elif command in commands['newChatCommands']:
                    if argument:
                        context_file = os.path.join('promts', current_branch, f'{argument}.json')
                        wright(f"Новый диалог создан для ветки '{current_branch}'.", say=outputText)
                    else:                    
                        context_file = os.path.join('promts', current_branch, 'newContext.json')
                        wright("Имя диалога не указано. Оно бутет создано автоматически.", say=outputText)    
                    with open(context_file, 'w', encoding='utf-8') as f:
                        json.dump([], f)  # Начинаем с пустого контекста

                elif command in commands['showChatsCommands']:
                    wright(showChats(current_branch), say=outputText)    

                elif command in commands['showCurrentChatCommands']:
                    wright(chat, True)

                elif command in commands['selectChatCommands']:
                    if argument:
                        chat_res = selectChat(current_branch, argument, outputText)
                        if chat_res:
                            chat = chat_res
                    else:
                        wright("Ошибка: укажите название чата для переключения.", say=outputText)   
                
                elif command in commands['restoreChatCommands']:
                    if argument:
                        try:
                            restore_chat(current_branch, argument)
                        except:
                            wright("Ошибка: укажите имя файла для восстановления диалога.", say=outputText)
                    else:
                        restore_chat(current_branch, f"{chat}.json")    
                # Ветки
                elif command in commands['newBranchCommands']:
                    if argument:
                        os.makedirs(os.path.join('promts', argument), exist_ok=True)
                        with open(os.path.join('promts', argument, 'context.json'), 'w', encoding='utf-8') as f:
                            json.dump([], f)
                        with open(os.path.join('promts', argument, 'mandatory_context.json'), 'w', encoding='utf-8') as f:
                            json.dump([{"role": "system", "content": "Высокий приоритет контексту: "}], f, ensure_ascii=False)
                        wright(f"Ветка '{argument}' создана.", say=outputText)
                    else:
                        wright("Имя ветки не указано.", say=outputText)    

                elif command in commands['showBranchCommands']:
                    wright(show_branches(), say=outputText)

                elif command in commands['showCurrentBranchCommands']:
                    wright(f"Текущая ветка: {current_branch}", say=outputText)

                elif command in commands['selectBranchCommands']:
                    if argument:
                        current_branch = argument
                        chat = 'context'
                        wright(f"Текущая ветка: {current_branch}, чат: {chat}", say=outputText)
                    else:
                        wright("Ошибка: укажите имя ветки для переключения.", say=outputText)
                # Скрипты
                elif any(command in item for sublist in scriptsNames.values() for item in sublist):
                    for script in scriptsNames.keys():
                        print(script, scriptsNames.keys())
                        if command in scriptsNames[script]:
                            runPrograms(script)
                # Голос
                elif command in commands['changeVoiceCommands']:
                    if config['voice'] == voices[0]:
                        config['voice'] = voices[1]
                    else:
                        config['voice'] = voices[0]
                    with open('config.json', 'w', encoding='utf-8') as file:
                        json.dump(config, file, indent=4, ensure_ascii=False)
                    wright(f"Голос изменен на {config['voice']}", say=outputText)
                
                elif command in commands['webCommands']:
                    response = requestTextAI(res, current_branch, chat, True)
                    outputText.put(response)
                    wright(response)
                    
            else:
                pass
                response = requestTextAI(res, current_branch, chat, False)
                outputText.put(response)
                wright(response)

            wright('------------')
    if active_timer:
        timer_stop_event.set()
        active_timer.join()
    wright("Остановка main", True)