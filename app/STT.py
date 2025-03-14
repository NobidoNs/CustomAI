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
AWAIT_TIME = 1

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    commands = devolp_config['commands']
    baitWords = devolp_config['baitWords']
    voskModelPath = devolp_config['voskModelPath']
    badWords = devolp_config['badWords']

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

def amplify_audio(audio_data, factor=5.0):
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
    audio_np *= factor
    audio_np = np.clip(audio_np, -32768, 32767).astype(np.int16)
    return audio_np.tobytes()

def is_speech(audio_data):
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    volume = np.abs(audio_np).mean()
    return volume > 300

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
    recognitionWords = f'[{wakeWordStr},{baitWordsStr},{muteCommandsStr},{badWordsStr}]'

    model = Model(voskModelPath)
    rec = KaldiRecognizer(model, SAMPLE_RATE, recognitionWords)

    partRes = False
    audio_buffer = collections.deque(maxlen=MAX_FRAMES)

    while not condition.is_set():
        data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
        data = amplify_audio(data)
        audio_buffer.append(data)

        if is_speech(data):
            last_speech_time = time.time()
            if rec.AcceptWaveform(data): 
                res = json.loads(rec.Result())['text']
                # print(res, commands['muteCommands'])
                if res in commands['muteCommands']:
                    queue.put(res)
                    partRes = False
                    audio_buffer.clear()
            else:
                partial_result = json.loads(rec.PartialResult())
                partial_text = partial_result.get("partial", "")

                if partial_text in wakeWord:
                    partRes = True
                    startListenTime = time.time()
                
                for word in badWords:
                    if word in partial_text:
                        threading.Thread(target=playSound, args=('sounds/pep.mp3',), daemon=True).start()    
                        print("PEP")    

        else:
            if partRes and time.time() - last_speech_time > AWAIT_TIME:
                wright('🎤', True)
                threading.Thread(target=recognize_speech_buffer, args=(queue, list(audio_buffer),time.time()-startListenTime + 1,), daemon=True).start()
                audio_buffer.clear()
                partRes = False
