from gtts import gTTS
from pygame import mixer
import time
import tempfile
import threading
import queue
import os

mixer.init()



def split_text(text, max_len):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if sum(len(w) for w in current_chunk) + len(word) <= max_len:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def generate_audio(text, index):
    tts = gTTS(text=text, lang="ru")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_path = temp_file.name
    tts.save(temp_path)
    audio_queue.put((index, temp_path))

def play_audio():
    while not stop_event.is_set():
        try:
            index, file_path = audio_queue.get(timeout=2)
        except queue.Empty:
            continue

        mixer.music.load(file_path)
        mixer.music.play()
        print("Время выполнения:", time.time() - start)
        play_event.set()  # Разрешаем генерации следующего куска

        while mixer.music.get_busy():
            time.sleep(0.05) 

        mixer.music.unload()
        os.remove(file_path)

        if audio_queue.empty():
            stop_event.set()  # Если больше файлов нет, завершаем



text = "Привет! Это тестовый текст, который мы будем разбивать по знакам препинания. Надеюсь, всё сработает хорошо! Давай проверим?"

if text[-1] == ".": text = text[:-1]
text_parts = text.split(".")

audio_queue = queue.Queue()
play_event = threading.Event()  # Управляет воспроизведением (чтобы не было задержек)
stop_event = threading.Event()

start = time.time()

# Запускаем поток воспроизведения
play_thread = threading.Thread(target=play_audio, daemon=True)
play_thread.start()

# Генерируем первую часть сразу
thread = threading.Thread(target=generate_audio, args=(text_parts[0], 0))
thread.start()
thread.join() 

# Запускаем оставшиеся части, пока первая играет
for i, part in enumerate(text_parts[1:], start=1):
    play_event.wait()  # Ждём, пока начнётся воспроизведение текущей
    play_event.clear()  # Сбрасываем, пока следующая часть не загрузится
    thread = threading.Thread(target=generate_audio, args=(part, i))
    thread.start()

play_thread.join()

