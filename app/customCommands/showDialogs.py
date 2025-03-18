import os
from app.utils.wright import wright

def showDialogs(branch):
    dialogues_dir = os.path.join('promts', branch)
    if not os.path.exists(dialogues_dir):
        wright("Ошибка: папка для диалогов не найдена.")
        return

    dialogues = [f for f in os.listdir(dialogues_dir) if f.endswith('.json')]
    if not dialogues:
        wright("Нет доступных диалогов в текущей ветке.")
    else:
        wright("Доступные диалоги:\n" + "\n".join(dialogues))