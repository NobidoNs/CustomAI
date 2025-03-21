import os
from app.utils.wright import wright

def showChats(branch):
    chats_dir = os.path.join('promts', branch)
    if not os.path.exists(chats_dir):
        wright("Ошибка: папка для диалогов не найдена.")
        return

    # Фильтруем файлы, исключая mandatory_context.json и убираем расширение .json
    chats = [os.path.splitext(f)[0] for f in os.listdir(chats_dir) 
                 if f.endswith('.json') and f != 'mandatory_context.json']
    
    if not chats:
        wright("Нет доступных диалогов в текущей ветке.")
    else:
        wright("Доступные диалоги:\n" + "\n".join(chats))