import json
import os

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)

BASE_CONTEXT_DIR = 'promts'

def save_context(context, branch):
    # Создаём папку для текущей ветки, если её нет
    context_dir = os.path.join(BASE_CONTEXT_DIR, branch)
    os.makedirs(context_dir, exist_ok=True)  # Создаёт папку, если её ещё нет
    context_file = os.path.join(context_dir, 'context.json')      

    # Сохраняем контекст в файл
    with open(context_file, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)       

def load_context(branch):
    # Загружаем контекст из соответствующей папки
    context_file = os.path.join(BASE_CONTEXT_DIR, branch, 'context.json')
    try:
        with open(context_file, 'r', encoding='utf-8') as f:      
            return json.load(f)
    except FileNotFoundError:
        return []  # Если файла нет, возвращаем пустой список

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