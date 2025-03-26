from pygame import mixer
import time
from app.utils.wright import wright
from app.customAI.TTS import process_text_with_ai
import tempfile
import asyncio
import threading
import queue
import os
import re
import json
import edge_tts
from pydub import AudioSegment

with open('devolp_config.json', 'r', encoding='utf-8') as file:
  devolp_config = json.load(file)
  useCutTTS = devolp_config["useCutTTS"]

with open('config.json', 'r', encoding='utf-8') as file:
  config = json.load(file)
  voice = config["voice"]
AUDIO_FREQUENCY = 48000
def text_cleaner(text):
    if not text:
        return ''
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

def change_pitch(audio_path, semitones):
    audio = AudioSegment.from_file(audio_path)
    pitch_change = 2 ** (semitones / 12.0)
    filtered = audio._spawn(audio.raw_data, overrides={
        'frame_rate': int(audio.frame_rate * pitch_change)
    })
    filtered.export(audio_path, format='mp3')

async def generate_audio(text, index, audio_queue, speed):
    output_path = tempfile.NamedTemporaryFile(suffix=".mp3").name
    if speed == 1:
        tts = edge_tts.Communicate(text=text, voice=voice)
    else:
        if speed < 1:
            speedRate = f'-{int((1-speed)*100)}%'
        else:
            speedRate = f'+{int((speed-1)*100)}%'
        tts = edge_tts.Communicate(text=text, voice=voice, rate=speedRate)
    
    await tts.save(output_path)

    if voice == "ru-RU-SvetlanaNeural":
        change_pitch(output_path, 3)

    audio_queue.put((index, output_path))

def play_audio(play_event, audio_queue, stop_event):
    while not stop_event.is_set():
        try:
            index, file_path = audio_queue.get(timeout=2)
        except queue.Empty:
            if stop_event.is_set():
                break
            continue

        try:
            mixer.music.load(file_path)
            mixer.music.play()

            play_event.set()

            while mixer.music.get_busy():
                if stop_event.is_set():  # Immediately interrupt
                    mixer.music.stop()
                    mixer.music.unload()
                    break
                time.sleep(0.05)

            mixer.music.unload()
        finally:
            # Always try to clean up the file, even if an error occurred
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass  # Ignore errors during cleanup

        if audio_queue.empty() or stop_event.is_set():
            break
    mixer.music.stop()
    mixer.music.unload()

def tts(inpText, inpCommand, condition):
    def process_inp_command():
        nonlocal speed  # Сделаем переменную speed доступной в этой функции
        if not inpCommand.empty():
            command = inpCommand.get()
            argument = command.split(' ', 1)[1] if ' ' in command else None
            if command == "stop":
                wright("Stopping audio playback.")
                mixer.music.stop()
                mixer.music.unload()
                time.sleep(0.5)
                stop_event.set()  # Сигнал остановки
                with audio_queue.mutex:
                    audio_queue.queue.clear()  # Очистка очереди
            elif command == "-mute":
                return "-mute"
            elif "-speed" in command:
                if argument == 'up':
                    speed += 0.5
                    wright(f"Установлена скорость {speed}", say=inpText)
                elif argument == 'down':
                    if  speed >= 1.5:
                        speed -= 0.5
                    else:
                        speed = 1.0
                    wright(f"Установлена скорость {speed}", say=inpText)
                else:
                    speed = float(argument)
                    if  speed < 1:
                        speed = 1.0
                    wright(f"Установлена скорость {speed}", say=inpText)
    
    if voice == "ru-RU-DmitryNeural":
        speed = 1.1
    else:    
        speed = 1.0
    audio_queue = queue.Queue()
    play_event = threading.Event()  # Управляет воспроизведением (чтобы не было задержек)
    stop_event = threading.Event()
    
    while not condition.is_set():
        time.sleep(0.1)
        process_inp_command()
        if not inpText.empty():
            stop_event.clear()
            stop_event = threading.Event()
            text = inpText.get()

            if useCutTTS:
                text = text_cleaner(process_text_with_ai(text))
            else:
                text = text_cleaner(text)

            text_parts = text.split(".")
            res_text_parts = []
            if text_parts[-1] == "." or text_parts[-1] == "": 
                text_parts = text_parts[:-1]
            for text_part in text_parts:
                chanks = split_text(text_part, 100)
                for chank in chanks:
                    res_text_parts.append(chank)
            text_parts = res_text_parts

            # Запускаем поток воспроизведения
            play_thread = threading.Thread(target=play_audio, args=(play_event, audio_queue, stop_event), daemon=True)
            play_thread.start()

            # Генерируем первую часть сразу
            thread = threading.Thread(target=asyncio.run, args=(generate_audio(text_parts[0], 0, audio_queue, speed),))
            thread.start()
            thread.join() 

            # Запускаем оставшиеся части, пока первая играет
            for i, part in enumerate(text_parts[1:], start=1):
                process_inp_command()
                if stop_event.is_set():
                    break

                play_event.wait()  # Ждём, пока начнётся воспроизведение текущей
                play_event.clear()  # Сбрасываем, пока следующая часть не загрузится
                thread = threading.Thread(target=asyncio.run, args=(generate_audio(part, 0, audio_queue, speed),))
                thread.start()

    
    wright("Остановка TTS", True)

# sound init 
mixer.init(frequency=AUDIO_FREQUENCY) # Инициализация с частотой
