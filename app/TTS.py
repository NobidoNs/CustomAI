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
import traceback

with open('devolp_config.json', 'r', encoding='utf-8') as file:
  devolp_config = json.load(file)
  useCutTTS = devolp_config["useCutTTS"]

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
    try:
        audio = AudioSegment.from_file(audio_path)
        pitch_change = 2 ** (semitones / 12.0)
        filtered = audio._spawn(audio.raw_data, overrides={
            'frame_rate': int(audio.frame_rate * pitch_change)
        })
        filtered.export(audio_path, format='mp3')
    except Exception as e:
        wright(f"Ошибка при изменении высоты тона: {e}", True)

async def generate_audio(text, index, audio_queue, speed, stop_event):
    try:
        if stop_event.is_set():
            return
            
        output_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name

        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
            voice = config["voice"]
        print(voice)
        if speed == 1:
            tts = edge_tts.Communicate(text=text, voice=voice)
        else:
            if speed < 1:
                speedRate = f'-{int((1-speed)*100)}%'
            else:
                speedRate = f'+{int((speed-1)*100)}%'
            tts = edge_tts.Communicate(text=text, voice=voice, rate=speedRate)
        
        await tts.save(output_path)

        if voice == "айка":
            change_pitch(output_path, 3)

        if not stop_event.is_set():
            audio_queue.put((index, output_path))
    except Exception as e:
        wright(f"Ошибка при генерации аудио: {e}", True)
        # Если произошла ошибка, но файл был создан, удаляем его
        try:
            if 'output_path' in locals() and os.path.exists(output_path):
                os.remove(output_path)
        except Exception:
            pass

def play_audio(play_event, audio_queue, stop_event):
    try:
        while not stop_event.is_set():
            try:
                # Получаем аудио из очереди с таймаутом
                try:
                    index, file_path = audio_queue.get(timeout=1)
                except queue.Empty:
                    continue
                
                # Проверяем флаг остановки
                if stop_event.is_set():
                    # Удаляем файл и продолжаем
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except Exception:
                        pass
                    continue
                
                # Проверяем существование файла
                if not os.path.exists(file_path):
                    wright("Файл аудио не найден", True)
                    continue
                
                # Загружаем и воспроизводим аудио
                try:
                    mixer.music.load(file_path)
                    
                    # Устанавливаем событие перед воспроизведением
                    play_event.set()
                    
                    mixer.music.play()
                    
                    # Ждем окончания воспроизведения или сигнала остановки
                    while mixer.music.get_busy():
                        if stop_event.is_set():
                            mixer.music.stop()
                            break
                        time.sleep(0.05)
                    
                    mixer.music.unload()
                except Exception as e:
                    wright(f"Ошибка при воспроизведении аудио: {e}", True)
                finally:
                    # Удаляем временный файл
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except Exception:
                        pass
            except Exception as e:
                wright(f"Ошибка в цикле воспроизведения: {e}", True)
                time.sleep(0.5)  # Пауза перед следующей итерацией
    except Exception as e:
        wright(f"Критическая ошибка в потоке воспроизведения: {e}", True)
        wright(traceback.format_exc(), True)
    finally:
        # Гарантированная очистка при выходе
        try:
            mixer.music.stop()
            mixer.music.unload()
        except Exception:
            pass

def tts(inpText, inpCommand, condition):
    def process_inp_command():
        nonlocal speed
        if inpCommand.empty():
            return None
            
        try:
            command = inpCommand.get()
            argument = command.split(' ', 1)[1] if ' ' in command else None
            
            if command == "stop":
                wright("Stopping audio playback.")
                
                # Останавливаем воспроизведение
                try:
                    mixer.music.stop()
                    mixer.music.unload()
                except Exception as e:
                    wright(f"Ошибка при остановке музыки: {e}", True)
                
                # Устанавливаем флаг остановки
                stop_event.set()
                
                # Очищаем очередь аудио
                try:
                    with audio_queue.mutex:
                        audio_queue.queue.clear()
                except Exception as e:
                    wright(f"Ошибка при очистке очереди: {e}", True)
                
                # Принудительно перезапускаем mixer
                try:
                    mixer.quit()
                    time.sleep(0.2)
                    mixer.init(frequency=AUDIO_FREQUENCY)
                except Exception as e:
                    wright(f"Ошибка при перезапуске mixer: {e}", True)
                
                return "stop"
            elif command == "-mute":
                return "-mute"
            elif "-speed" in command:
                try:
                    if argument == 'up':
                        speed += 0.5
                        wright(f"Установлена скорость {speed}", say=inpText)
                    elif argument == 'down':
                        if speed >= 1.5:
                            speed -= 0.5
                        else:
                            speed = 1.0
                        wright(f"Установлена скорость {speed}", say=inpText)
                    else:
                        try:
                            speed = float(argument)
                            if speed < 1:
                                speed = 1.0
                            wright(f"Установлена скорость {speed}", say=inpText)
                        except ValueError:
                            wright("Неверный формат скорости", say=inpText)
                except Exception as e:
                    wright(f"Ошибка при изменении скорости: {e}", True)
        except Exception as e:
            wright(f"Ошибка при обработке команды: {e}", True)
            
        return None
    
    try:
        # Инициализация переменных
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
            voice = config["voice"]
        if voice == "джарвис":
            speed = 1.1
        else:    
            speed = 1.0
        
        audio_queue = queue.Queue()
        play_event = threading.Event()
        stop_event = threading.Event()
        play_thread = None
        
        # Основной цикл
        while not condition.is_set():
            try:
                time.sleep(0.1)
                
                # Обработка команд
                cmd_result = process_inp_command()
                if cmd_result == "stop":
                    continue
                
                # Обработка текста
                if not inpText.empty():
                    # Останавливаем предыдущее воспроизведение
                    stop_event.set()
                    
                    # Очищаем очередь
                    with audio_queue.mutex:
                        audio_queue.queue.clear()
                    
                    # Ждем завершения потока воспроизведения
                    if play_thread and play_thread.is_alive():
                        play_thread.join(timeout=1.0)
                    
                    # Сбрасываем события
                    play_event.clear()
                    stop_event = threading.Event()  # Создаем новый объект события
                    
                    # Получаем и обрабатываем текст
                    text = inpText.get()

                    if not isinstance(text, str):
                        continue

                    text = text.replace('\n', ' ')  # Заменяем переносы строк
                    
                    if useCutTTS:
                        text = text_cleaner(process_text_with_ai(text))
                    else:
                        text = text_cleaner(text)
                    
                    if not text:
                        continue
                    
                    # Разбиваем текст на части
                    text_parts = []
                    for sentence in re.split(r'(?<=[.!?])\s+', text):
                        if sentence.strip():
                            chunks = split_text(sentence, 200)
                            for chunk in chunks:
                                if chunk.strip():
                                    text_parts.append(chunk)
                    
                    if not text_parts:
                        continue
                    
                    # Запускаем поток воспроизведения
                    play_thread = threading.Thread(
                        target=play_audio, 
                        args=(play_event, audio_queue, stop_event), 
                        daemon=True
                    )
                    play_thread.start()
                    
                    # Обрабатываем каждую часть текста
                    for i, part in enumerate(text_parts):
                        # Проверяем команды и флаг остановки
                        if process_inp_command() == "stop" or stop_event.is_set():
                            break
                        
                        # Генерируем аудио для текущей части
                        asyncio.run(generate_audio(part, i, audio_queue, speed, stop_event))
                        
                        # Для всех частей, кроме последней, ждем начала воспроизведения
                        if i < len(text_parts) - 1:
                            # Ждем с таймаутом и периодическими проверками
                            wait_start = time.time()
                            while time.time() - wait_start < 10.0:
                                if play_event.wait(timeout=0.5):
                                    play_event.clear()
                                    break
                                
                                if stop_event.is_set():
                                    break
                                
                                # Если очередь пуста и ничего не воспроизводится,
                                # возможно, произошла ошибка
                                if audio_queue.empty() and not mixer.music.get_busy():
                                    break
            except Exception as e:
                wright(f"Ошибка в основном цикле TTS: {e}", True)
                wright(traceback.format_exc(), True)
                time.sleep(1)
    except Exception as e:
        wright(f"Критическая ошибка в TTS: {e}", True)
        wright(traceback.format_exc(), True)
    finally:
        # Очистка ресурсов
        try:
            stop_event.set()
            
            with audio_queue.mutex:
                audio_queue.queue.clear()
            
            if play_thread and play_thread.is_alive():
                play_thread.join(timeout=1.0)
            
            mixer.music.stop()
            mixer.music.unload()
        except Exception as e:
            wright(f"Ошибка при очистке ресурсов: {e}", True)
        
        wright("Остановка TTS", True)

# Инициализация звука
try:
    mixer.init(frequency=AUDIO_FREQUENCY)
except Exception as e:
    wright(f"Ошибка при инициализации mixer: {e}", True)
