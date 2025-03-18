import os
from app.utils.wright import wright

def selectDialog(branch, new_dialog):
    dialog_file = os.path.join('promts', branch, f'{new_dialog}.json')
    if os.path.exists(dialog_file):
        wright(f"Переключение на чат '{new_dialog}' в ветке '{branch}'.")
        return new_dialog
    else:
        wright(f"Ошибка: чат '{new_dialog}' не найден в ветке '{branch}'.")
        return None