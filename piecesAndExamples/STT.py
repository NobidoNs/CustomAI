import os
import pyaudio
from vosk import Model, KaldiRecognizer

# Путь к модели Vosk
model_path = '/home/nobidon/Документы/GitHub/CustomAI/vosk-model-small-ru-0.22'

if not os.path.exists(model_path):
    print(f"Модель не найдена по пути {model_path}. Скачайте модель с https://alphacephei.com/vosk/models.")
    exit(1)

# Загрузка модели
model = Model(model_path)

# Настройки аудиопотока
FORMAT = pyaudio.paInt16  # Формат аудио
CHANNELS = 1  # Моно
RATE = 16000  # Частота дискретизации
CHUNK = 8192  # Размер блока данных

# Инициализация PyAudio
p = pyaudio.PyAudio()

# Открытие аудиопотока
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Инициализация распознавателя
rec = KaldiRecognizer(model, RATE)

print("Говорите... (нажмите Ctrl+C для остановки)")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = rec.Result()
            print("Распознано:", result)
        else:
            partial_result = rec.PartialResult()
            print("Частично распознано:", partial_result)

except KeyboardInterrupt:
    print("\nЗавершение работы...")

finally:
    # Остановка и закрытие потока
    stream.stop_stream()
    stream.close()
    p.terminate()