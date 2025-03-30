import os
from app.utils.write import write

def selectBranch(branch, say):
    chat_file = os.path.join('promts', branch, f'context.json')
    if os.path.exists(chat_file):
        write(f"Переключение на ветку '{branch}'.", say=say)
        return branch
    else:
        write(f"Ошибка: ветка '{branch}' не найдена.", say=say)
        return None