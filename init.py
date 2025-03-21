import json

try:
    with open('config.json', 'r+', encoding='utf-8') as file:
        config = json.load(file)
except:
    print("Не удалось загрузить файл config.json")
    print("У программы недостаточно прав")
    exit()

try:
    with open('devolp_config.json', 'r+', encoding='utf-8') as file:
        devolp_config = json.load(file)
except:
    print("Не удалось загрузить файл devolp_config.json")
    exit()

def run_init():
    try:
        open('output.md', 'a+').close()
    except:
        print("Не удалось создать файл output.md")
        print("Создайте в папке проекта файл output.md")

    if input("Использовать настройку по умолчанию? (Y/n): ").strip().lower() == "n":
        config['wakeWord'] = input("Введите слово (имя) для активации: ")
        wt =  int(input("Введите время ожидания голосового ввода (в секундах): "))
        if wt:
            config['waitTime'] = wt
        if input("Использовать звук старта? (Y/n): ").strip().lower() == "n":
            config['soundStart'] = ''
            if input("Использовать собственный звук старта? (y/N): ").strip().lower() == "y":
                config['soundStart'] = input("Введите путь к звуку: ")
        
        # if input("Интеграция с Zapret (y/N): ").strip().lower() == "y":
        #     config['useZapret'] = True
        #     config['zapretPath'] = input("Введите путь к файлу zapret.exe: ")
        #     config['zapretProcess'] = input("Введите название процесса: ")
        #     if not config['zapretPath'] or not config['zapretProcess']:
        #         print("Отмена интеграции с Zapret")
        #         config['useZapret'] = False
    else:
        print("Имя ассистента - Джарвис")
        print("Для команд --help или 'расскажи что умеешь'")

    # Применяем изменения в файлы
    devolp_config["init"] = True
    
    with open('config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
    
    with open('devolp_config.json', 'w', encoding='utf-8') as file:
        json.dump(devolp_config, file, indent=4, ensure_ascii=False)
