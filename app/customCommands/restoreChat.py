import os
import json
from app.utils.write import write

def restore_chat(branch, file_name):
    file_path = os.path.join('promts', branch, file_name)

    if not os.path.exists(file_path):
        write(f"Ошибка: файл '{file_name}' не найден в ветке '{branch}'.", log=True)
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        context = json.load(f)

    context_file = 'output.md'
    with open(context_file, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
