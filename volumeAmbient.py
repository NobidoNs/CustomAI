import pyaudio
import numpy as np
import time

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

try:
    while True:
        volume_levels = []  # Буфер громкости
        start_time = time.time()

        while time.time() - start_time < DURATION:
            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16)
            
            volume = np.mean(np.abs(samples))  # Средняя абсолютная громкость
            # print(volume)
            volume_levels.append(volume)

        avg_volume = np.median(volume_levels)  # Берем медиану для сглаживания выбросов
        print(f"Средняя громкость за {DURATION} секунд: {avg_volume:.2f}")
        print(f"устанивите значение volumeAmbient в devolp_config {int(avg_volume)*1.5} выбирайте меньшее")

except KeyboardInterrupt:
    print("\nОстановка измерения громкости.")

# Закрытие потока
stream.stop_stream()
stream.close()
audio.terminate()
