import os
from app.utils.wright import wright

def selectChat(branch, new_chat):
    chat_file = os.path.join('promts', branch, f'{new_chat}.json')
    if os.path.exists(chat_file):
        wright(f"Переключение на чат '{new_chat}' в ветке '{branch}'.")
        return new_chat
    else:
        wright(f"Ошибка: чат '{new_chat}' не найден в ветке '{branch}'.")
        return None