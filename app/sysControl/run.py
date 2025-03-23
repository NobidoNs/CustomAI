import subprocess
import os
import platform
import psutil

def close_program(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] == process_name:
                print(f"Закрытие процесса: {proc.info['name']} (PID: {proc.info['pid']})")
                proc.terminate()  # Завершаем процесс
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def runPrograms(script):
    close = False
    # Путь к файлу с командами
    file_path = os.path.join("app", "sysControl", f"{script}.txt")

    # Открываем файл и читаем команды
    with open(file_path, "r", encoding="utf-8") as file:
        commands = file.readlines()

    # Определяем текущую операционную систему
    system = platform.system().lower()

    # Выполняем каждую команду
    for command in commands:
        command = command.strip()  # Убираем лишние пробелы и символы новой строки
        if not command:  # Пропускаем пустые строки
            continue

        print(f"Выполняется команда: {command}")
        if command == 'close':
            close = True
            continue
        if close == True:
            close_program(command)
            continue
        
        try:
            # Обработка URI-ссылок (например, steam://)
            if command.startswith(("steam://", "http://", "https://")):
                if system == "windows":
                    subprocess.run(["start", command], shell=True, check=True)
                elif system == "linux":
                    subprocess.run(["xdg-open", command], check=True)
                elif system == "darwin":  # macOS
                    subprocess.run(["open", command], check=True)
                else:
                    print(f"Неизвестная ОС: {system}. Невозможно открыть URI.")
                continue

            # Обработка обычных команд
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды: {e}")
