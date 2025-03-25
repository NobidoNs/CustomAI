from vosk import Model, KaldiRecognizer
import pyaudio
import speech_recognition as sr
import time
import json
import collections
import numpy as np
import threading
from app.utils.wright import wright
from app.utils.playSound import playSound

# Настройки аудиопотока
FORMAT = pyaudio.paInt16 
CHANNELS = 1 
SAMPLE_RATE = 16000
BUFFER_SIZE = 4096
AUDIO_DURATION = 60  # В секундах
MAX_FRAMES = (SAMPLE_RATE // BUFFER_SIZE) * AUDIO_DURATION
AWAIT_TIME = 1.5

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    commands = devolp_config['commands']
    baitWords = devolp_config['baitWords']
    voskModelPath = devolp_config['voskModelPath']
    badWords = devolp_config['badWords']
    volumeAmbient = devolp_config['volumeAmbient']

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    wakeWord = config['wakeWord']
    waitTime = config['waitTime']

def makeStream():
    # Инициализация PyAudio
    p = pyaudio.PyAudio()

    # Открытие аудиопотока
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=BUFFER_SIZE)
    return stream

def normalize_volume(audio_bytes, target_rms=1500, max_gain=5.0, dtype=np.int16):
    audio_data = np.frombuffer(audio_bytes, dtype=dtype)

    if len(audio_data) == 0:
        return audio_bytes
    
    rms = np.sqrt(np.mean(audio_data.astype(np.float32) ** 2))
    if rms < 300:  # Порог "тишины" (можно регулировать)
        gain = min(target_rms / (rms + 1e-6), max_gain)  # Ограничиваем усиление
        normalized_data = (audio_data * gain).astype(dtype)
    else:
        normalized_data = audio_data
    
    return normalized_data.tobytes()

def calibrate_threshold(stream, calibration_duration=2.0):
    startTime = time.time()
    audio_data = bytearray()
    while time.time()-startTime < calibration_duration:
        data = normalize_volume(stream.read(BUFFER_SIZE, exception_on_overflow=False))
        audio_data.extend(data)
        if not data:
            break

    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    calibration_samples = int(calibration_duration * SAMPLE_RATE)
    calibration_audio = audio_np[:calibration_samples]
    noise_level = np.abs(calibration_audio).mean()
    threshold = noise_level * 1.2
    return threshold

def is_speech(audio_data, threshold):
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    volume = np.abs(audio_np).mean()
    # print(f"Volume: {volume}, Threshold: {threshold}")
    return volume > threshold

def get_last_seconds_audio(seconds, buffer_data):
    chunks_needed = int((SAMPLE_RATE * seconds) / BUFFER_SIZE)
    if len(buffer_data) == 0:
        print("⚠️ Буфер пуст, нечего извлекать!")
        return None
    if chunks_needed <= 0 or chunks_needed > len(buffer_data):
        chunks_needed = len(buffer_data) 

    total_samples = len(buffer_data) * BUFFER_SIZE
    actual_duration = total_samples / SAMPLE_RATE
    
    print(f"📊 Audio duration: {actual_duration:.2f} seconds (запрашиваем {seconds} сек)")


    audio_data = b''.join(buffer_data[-chunks_needed:])
    return sr.AudioData(audio_data, SAMPLE_RATE, 2)

def recognize_speech_buffer(queue, audio_buffer, listenTime):
    googleRec = sr.Recognizer()

    audio_data = b''.join(audio_buffer)
    audio_data = sr.AudioData(audio_data, SAMPLE_RATE, 2)
    audio_data = get_last_seconds_audio(listenTime, audio_buffer)

    
    # with open("TEMPoutputTEMP.wav", "wb") as f:
    #     f.write(audio_data.get_wav_data())
    try:
        text = googleRec.recognize_google(audio_data, language="ru-RU")
        queue.put(text)
    except:
        wright('❌ Google Speech не распознал речь', True)



def listenCommand(queue,condition,stream): # Listen for wake word and commands
    # some boring converting
    wakeWordStr = ",".join(f'"{item}"' for item in wakeWord)
    baitWordsStr = ",".join(f'"{item}"' for item in baitWords)
    muteCommandsStr = ",".join(f'"{item}"' for item in commands['muteCommands'])
    badWordsStr = ",".join(f'"{item}"' for item in badWords)
    if badWordsStr == '':
        recognitionWords = f'[{wakeWordStr},{baitWordsStr},{muteCommandsStr}]'
        
    else:
        recognitionWords = f'[{wakeWordStr},{baitWordsStr},{muteCommandsStr},{badWordsStr}]'

    model = Model(voskModelPath)
    rec = KaldiRecognizer(model, SAMPLE_RATE, recognitionWords)

    partRes = False
    wake_sound_played = False
    stop_sound_played = False
    audio_buffer = collections.deque(maxlen=MAX_FRAMES)

    if volumeAmbient == 0:
        threshold = calibrate_threshold(stream, calibration_duration=0.5)
    else:
        threshold = volumeAmbient
    wright(f"🔊 Threshold: {threshold}", log=True)

    while not condition.is_set():
        data = stream.read(BUFFER_SIZE, exception_on_overflow=False)

        if is_speech(data, threshold):
            last_speech_time = time.time()
        else:
            if partRes and time.time() - last_speech_time > AWAIT_TIME:
                wright('🎤', True)
                partRes = False
                
                threading.Thread(target=playSound, args=('sounds/caset.mp3',), daemon=True).start()   
                threading.Thread(target=recognize_speech_buffer, args=(queue, list(audio_buffer), time.time() - startListenTime + 1,), daemon=True).start()
                audio_buffer.clear()
                wake_sound_played = False 

        data = normalize_volume(data)
        audio_buffer.append(data)
        
        if rec.AcceptWaveform(data): 
            res = json.loads(rec.Result())['text']
            
        else:
            partial_result = json.loads(rec.PartialResult())
            partial_text = partial_result.get("partial", "")
            # print(f"🔊 {partial_text}")
            if partial_text.startswith(tuple(commands['muteCommands'])) and not stop_sound_played:
                queue.put(partial_text)
                stop_sound_played = True

            if partial_text in wakeWord and not wake_sound_played:
                stop_sound_played = False
                partRes = True
                startListenTime = time.time()
                threading.Thread(target=playSound, args=('sounds/analog-button.mp3',), daemon=True).start()
                wake_sound_played = True

            for word in badWords:
                if any(word in partial_text.split() for word in badWords):
                    threading.Thread(target=playSound, args=('sounds/pep.mp3',), daemon=True).start()    

        
                

    wright("Остановка STT", True)