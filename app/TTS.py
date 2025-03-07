from pygame import mixer
from gtts import gTTS
import time
from app.utils.wright import wright
import tempfile
import threading
import queue
import os
import re
import json

with open('devolp_config.json', 'r') as file:
  devolp_config = json.load(file)
  AUDIO_FREQUENCY = devolp_config["AUDIO_FREQUENCY"]

def text_cleaner(text):
    text = re.sub(r'[^a-zA-Zа-яА-Я0-9\s\.,!?+-ё]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r',+', ',', text)
    return text

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

def generate_audio(text, index, audio_queue):
    tts = gTTS(text=text, lang="ru")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_path = temp_file.name
    tts.save(temp_path)
    audio_queue.put((index, temp_path))

def play_audio(play_event, audio_queue, stop_event, inpCommand):
    while not stop_event.is_set():
        try:
            index, file_path = audio_queue.get(timeout=2)
        except queue.Empty:
            continue

        mixer.music.load(file_path)
        mixer.music.play()
        play_event.set()  

        while mixer.music.get_busy():
            # Check commands during playback
            if not inpCommand.empty():
                command = inpCommand.get()
                if command == "stop":
                    wright("Stopping audio playback.", True)
                    mixer.music.stop()
                    stop_event.set()
                    break
            time.sleep(0.05)

        mixer.music.unload()
        os.remove(file_path)

        if audio_queue.empty():
            stop_event.set()

def tts(inpText, inpCommand, condition):
    speed = 1
    audio_queue = queue.Queue()
    play_event = threading.Event()  # Управляет воспроизведением (чтобы не было задержек)
    stop_event = threading.Event()
    
    while not condition.is_set():
        
        if not inpCommand.empty():
            command = inpCommand.get()
            argument = command.split(' ', 1)[1] if ' ' in command else None
            if command == "stop":
                mixer.music.stop()
                wright("Stopping audio playback.", True)
                stop_event.set()
            elif command == "-mute":
                break
            elif "-speed" in command:
                if argument == 'up':
                    speed += 0.5
                elif argument == 'down':
                    speed -= 0.5
                else:
                    speed = float(argument)
                wright(f'Speed set to {speed}')
        elif not inpText.empty():

            stop_event.clear()
            stop_event = threading.Event()
            text = inpText.get()
            
            text = text_cleaner(text)
            text_parts = text.split(".")
            res_text_parts = []
            if text_parts[-1] == "." or text_parts[-1] == "": text_parts = text_parts[:-1]
            for text_part in text_parts:
                chanks = split_text(text_part, 50)
                for chank in chanks:
                    res_text_parts.append(chank)
            text_parts = res_text_parts

            # Запускаем поток воспроизведения
            play_thread = threading.Thread(target=play_audio, args=(play_event, audio_queue, stop_event, inpCommand), daemon=True)
            play_thread.start()

            # Генерируем первую часть сразу
            thread = threading.Thread(target=generate_audio, args=(text_parts[0], 0, audio_queue))
            thread.start()
            thread.join() 

            # Запускаем оставшиеся части, пока первая играет
            for i, part in enumerate(text_parts[1:], start=1):
                play_event.wait()  # Ждём, пока начнётся воспроизведение текущей
                play_event.clear()  # Сбрасываем, пока следующая часть не загрузится
                thread = threading.Thread(target=generate_audio, args=(part, i, audio_queue))
                thread.start()

            play_thread.join()
    

# sound init 
mixer.init(frequency=AUDIO_FREQUENCY) # the sound seems to have changed
