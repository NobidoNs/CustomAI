import pyaudio
import numpy as np
import time
import json

with open('devolp_config.json', 'r+', encoding='utf-8') as file:
    devolp_config = json.load(file)

# Параметры записи
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
CHUNK = 1024
DURATION = 1  # Время усреднения (сек)

# Инициализация PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print(f"Измерение средней громкости за {DURATION} секунд (нажмите Ctrl+C для выхода)")
all = []
try:
    for i in range(5):
        volume_levels = []  # Буфер громкости
        start_time = time.time()

        while time.time() - start_time < DURATION:
            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16)
            
            volume = np.mean(np.abs(samples))  # Средняя абсолютная громкость
            # print(volume)
            volume_levels.append(volume)

        avg_volume = np.median(volume_levels)*1.5  # Берем медиану для сглаживания выбросов
        # print(f"Средняя громкость за {DURATION} секунд: {avg_volume:.2f}")
        print(f"Значение volumeAmbient в devolp_config {int(avg_volume)} (устаноится автоматически)")
        all.append(avg_volume)

except KeyboardInterrupt:
    print("\nОстановка измерения громкости.")

# Закрытие потока
stream.stop_stream()
stream.close()
audio.terminate()

devolp_config['volumeAmbient'] = int(np.median(all))
with open('devolp_config.json', 'w', encoding='utf-8') as file:
    json.dump(devolp_config, file, indent=4, ensure_ascii=False)
