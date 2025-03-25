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
        ww = input("Введите слово (имя) для активации (Джарвис): ").strip()
        if ww:
            config['wakeWord'] = [ww]
        
        wt = input("Введите время ожидания голосового ввода (в секундах) (1.5): ").strip()
        if wt:
            config['waitTime'] = int(wt)
        
        if input("Использовать звук старта? (Y/n): ").strip().lower() == "n":
            config['soundStart'] = ''
            if input("Использовать собственный звук старта? (y/N): ").strip().lower() == "y":
                config['soundStart'] = input("Введите путь к звуку: ").strip()
        
        # Добавление выбора голоса
        print("Доступные голоса:")
        for i, voice in enumerate(devolp_config["voices"], start=1):
            print(f"{i}. {voice}")
        
        voice_choice = int(input("Выберите голос (введите номер): ").strip())
        if 1 <= voice_choice <= len(devolp_config["voices"]):
            config["voice"] = devolp_config["voices"][voice_choice - 1]
        else:
            print("Некорректный выбор. Установлен голос по умолчанию.")
            config["voice"] = devolp_config["voices"][0]
    else:
        print("Имя ассистента - Джарвис")
        print("Для команд --help или 'расскажи что умеешь'")
    
    # Применяем изменения в файлы
    devolp_config["init"] = True
    
    with open('config.json', 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4, ensure_ascii=False)
    
    with open('devolp_config.json', 'w', encoding='utf-8') as file:
        json.dump(devolp_config, file, indent=4, ensure_ascii=False)
