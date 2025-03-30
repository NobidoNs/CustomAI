import os
from app.utils.write import write

def selectChat(branch, new_chat, say):
    chat_file = os.path.join('promts', branch, f'{new_chat}.json')
    if os.path.exists(chat_file):
        write(f"Переключение на чат '{new_chat}' в ветке '{branch}'.", say=say)
        return new_chat
    else:
        write(f"Ошибка: чат '{new_chat}' не найден в ветке '{branch}'.", say=say)
        return None