import json
import os

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)

BASE_CONTEXT_DIR = 'promts'

def save_context(context, branch, chat):
    # Создаём папку для текущей ветки, если её нет
    context_dir = os.path.join(BASE_CONTEXT_DIR, branch)
    os.makedirs(context_dir, exist_ok=True)  # Создаёт папку, если её ещё нет
    context_file = os.path.join(context_dir, f'{chat}.json')      

    # Сохраняем контекст в файл
    with open(context_file, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)       

def load_context(branch, chat):
    # Путь к основному контексту
    context_file = os.path.join(BASE_CONTEXT_DIR, branch, f'{chat}.json')

    # Путь к обязательному контексту
    mandatory_context_file = os.path.join(BASE_CONTEXT_DIR, branch, 'mandatory_context.json')

    # Загружаем основной контекст
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            context = json.load(f)
    except FileNotFoundError:
        context = []  # Если файла нет, возвращаем пустой список
    
    # Загружаем обязательный контекст
    mandatory_context = []
    try:
        with open(mandatory_context_file, 'r', encoding='utf-8') as f:
            mandatory_context = json.load(f)
    except FileNotFoundError:
        pass  # Если файла нет, просто игнорируем

    # Объединяем обязательный контекст с основным
    return mandatory_context + context

def load_code_files():
    code_context = []
    code_dir = "app"

    for filename in os.listdir(code_dir):
        if filename.endswith(".py"): 
            with open(os.path.join(code_dir, filename), "r", encoding="utf-8") as file:
                code_context.append(f"### {filename} ###\n{file.read()}\n")
    
    code_dir = "app/customCommands"
    for filename in os.listdir(code_dir):
        if filename.endswith(".py"): 
            with open(os.path.join(code_dir, filename), "r", encoding="utf-8") as file:
                code_context.append(f"### {filename} ###\n{file.read()}\n")
    
    code_dir = "app/utils"
    for filename in os.listdir(code_dir):
        if filename.endswith(".py"): 
            with open(os.path.join(code_dir, filename), "r", encoding="utf-8") as file:
                code_context.append(f"### {filename} ###\n{file.read()}\n")
    
    with open("devolp_config.json", "r", encoding="utf-8") as file:
        code_context.append(f"### devolp_config.json ###\n{file.read()}\n")
    with open("config.json", "r", encoding="utf-8") as file:
        code_context.append(f"### config.json ###\n{file.read()}\n")
    

    return "\n".join(code_context) 