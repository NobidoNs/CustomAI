import time
import os
import re
import json
import threading
from app.config import allCommands
from app.utils.write import write
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
from app.customCommands.selectBranch import selectBranch
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
    if jarv in wakeWord or jarv == 'чарльз':
        phrase = ' '.join(phrase.split()[1:]).lower()
    elif jarv == 'джар':
        jarv2 = phrase.split()[1].lower()
        if jarv2 == 'раз' or jarv2 == 'рас':
            phrase = ' '.join(phrase.split()[2:]).lower()
        else:
            phrase = ' '.join(phrase.split()[1:]).lower()
    # print(phrase, command)

    if phrase.lower().startswith(command):
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
                write(res)

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
                    write('stop')
                    commandToSound.put('stop')

                elif command in commands['disableTTS']:
                    write('MUTE', log=True)
                    commandToSound.put('-mute')

                elif command in commands['clearCliCommands']:
                    clearFile()
                    continue

                elif command in commands['rememberCommands']:
                    mand_path = f"promts/{current_branch}/mandatory_context.json"
                    with open(mand_path, 'r', encoding='utf-8') as file:
                        existing_data = json.load(file)
                    with open(mand_path, "w", encoding='utf-8') as file:
                        new_data =  {"role": "user", "content": f"Высокий приоритет контексту {argument}. Запомни это: {argument}"}
                        new_data2 = {"role": "user", "content": f"Запомни и это: {argument}"}
                        existing_data.append(new_data)
                        existing_data.append(new_data2)
                        json.dump(existing_data, file, ensure_ascii=False)
                    if config['voice'] == 'джарвис':
                        write(f'{argument}, Я запомнил', say=outputText)
                    else:
                        write(f'{argument}, Я запомнилa', say=outputText)

                elif command in commands['backupCommands']:
                    backup_file = saveBackup(argument)
                    write(f'Backup saved as: {backup_file}', log=True)

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
                    write(f"Контекст для ветки '{current_branch}' очищен.", say=outputText)

                elif command in commands['exitCommands']:
                    condition.set()

                elif command in commands['helpCommands']:
                    text_help = text_commands_help()
                    outputText.put(text_help)
                
                elif command in commands['aboutCommands']:
                    write(voice_commands_help(), say=outputText)
                    
                
                # Таймер
                elif command in commands['setTimerCommands']:
                    if argument:
                        timer_seconds = convertTime(argument)
                        if timer_seconds == 0:
                            write("Не удалось преобразовать время в секунды.", say=outputText)
                            continue
                        if active_timer:
                            timer_stop_event.set()
                            active_timer.join() 
                        timer_stop_event.clear()
                        write(f"Таймер установлен на {timer_seconds} секунд.", say=outputText)
                        active_timer = threading.Thread(target=timer, args=(timer_seconds, timer_stop_event), daemon=True)
                        active_timer.start()
                    else:
                        write("Ошибка: укажите время для таймера.", say=outputText)

                elif command in commands['stopTimerCommands']:
                    if active_timer: 
                        timer_stop_event.set() 
                        active_timer.join()
                        write("Таймер остановлен.", say=outputText)
                    else:
                        write("Таймер не запущен.", say=outputText)
                
                # Чаты
                elif command in commands['newChatCommands']:
                    if argument:
                        context_file = os.path.join('promts', current_branch, f'{argument}.json')
                        write(f"Новый диалог создан для ветки '{current_branch}'.", say=outputText)
                    else:                    
                        context_file = os.path.join('promts', current_branch, 'newContext.json')
                        write("Имя диалога не указано. Оно бутет создано автоматически.", say=outputText)    
                    with open(context_file, 'w', encoding='utf-8') as f:
                        json.dump([], f)  # Начинаем с пустого контекста

                elif command in commands['showChatsCommands']:
                    chats = showChats(current_branch)
                    # ruChats = re.sub(r'[a-zA-Z_]', '', chats)
                    # write(chats, log=True)
                    # write(ruChats, say=outputText)    
                    write(chats, say=outputText)

                elif command in commands['showCurrentChatCommands']:
                    write(chat, True)

                elif command in commands['selectChatCommands']:
                    if argument:
                        chat_res = selectChat(current_branch, argument, outputText)
                        if chat_res:
                            chat = chat_res
                    else:
                        write("Ошибка: укажите название чата для переключения.", say=outputText)   
                
                elif command in commands['restoreChatCommands']:
                    if argument:
                        try:
                            restore_chat(current_branch, argument)
                        except:
                            write("Ошибка: укажите имя файла для восстановления диалога.", say=outputText)
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
                        write(f"Ветка '{argument}' создана.", say=outputText)
                    else:
                        write("Имя ветки не указано.", say=outputText)    

                elif command in commands['showBranchCommands']:
                    branches = show_branches()
                    # ruBranches = re.sub(r'[a-zA-Z_]', '', branches)
                    # write(branches, log=True)
                    # write(ruBranches, say=outputText)
                    write(branches, say=outputText) 

                elif command in commands['showCurrentBranchCommands']:
                    write(f"Текущая ветка: {current_branch}", say=outputText)

                elif command in commands['selectBranchCommands']:
                    if argument:
                        branch_res = selectBranch(argument, outputText)
                        if branch_res:
                            current_branch = branch_res
                            chat = 'context'
                    else:
                        write("Ошибка: укажите имя ветки для переключения.", say=outputText)
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
                    write(f"Голос изменен на {config['voice']}", say=outputText)
                
                elif command in commands['webCommands']:
                    response = requestTextAI(res, current_branch, chat, True)
                    outputText.put(response)
                    write(response)
                    
            else:
                pass
                response = requestTextAI(res, current_branch, chat, False)
                outputText.put(response)
                write(response)

            write('------------')
    if active_timer:
        timer_stop_event.set()
        active_timer.join()
    write("Остановка main", True)