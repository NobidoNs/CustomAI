import subprocess
import os

# Путь к Update.exe
update_exe_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Discord', 'Update.exe')

# Запуск Discord
try:
    subprocess.run([update_exe_path, '--processStart', 'Discord.exe'], check=True)
    print("Discord запущен успешно.")
except subprocess.CalledProcessError as e:
    print(f"Ошибка при запуске Discord: {e}")