import os
from app.utils.write import write

def showChats(branch):
    chats_dir = os.path.join('promts', branch)
    if not os.path.exists(chats_dir):
        return "Ошибка: папка для диалогов не найдена."
        

    # Фильтруем файлы, исключая mandatory_context.json и убираем расширение .json
    chats = [os.path.splitext(f)[0] for f in os.listdir(chats_dir) 
                 if f.endswith('.json') and f != 'mandatory_context.json']
    
    if not chats:
        return "Нет доступных диалогов в текущей ветке."
    else:
        return "Доступные диалоги:\n" + "\n".join(chats)