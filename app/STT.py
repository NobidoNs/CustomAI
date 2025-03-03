from vosk import Model, KaldiRecognizer
import pyaudio
import speech_recognition as sr
import time
import json
from config import waitTime, wakeWord, baitWords, commands, voskModelPath
from app.public.wright import wright

def listenAll(startTime,queue):
    googleRec = sr.Recognizer()
    while time.time()-startTime<waitTime:
        with sr.Microphone() as source:
            audio = googleRec.listen(source)
        try:
            text = googleRec.recognize_google(audio, language="ru-RU")
            queue.put(text)
            
            startTime = time.time()
        except:
            pass

        with sr.Microphone() as source:
            audio = googleRec.listen(source)

def listenCommand(queue,condition):
    print('Listening...')
    recognizer = KaldiRecognizer(model, 16000, recognitionWords)

    while not condition.is_set():
        data = stream.read(8192,False)
        if recognizer.AcceptWaveform(data): 
            res = json.loads(recognizer.Result())["text"]
            print(res)
            if res in wakeWord:
                  wright('ON')
                #   tts('да')
                  listenAll(time.time(),queue)
                  wright('OFF')
                #   tts('отключаюсь')
            elif res in commands['muteCommands']:
                queue.put(res)




# some boring converting
wakeWordStr = ",".join(f'"{item}"' for item in wakeWord)
baitWordsStr = ",".join(f'"{item}"' for item in baitWords)
muteCommandsStr = ",".join(f'"{item}"' for item in commands['muteCommands'])
recognitionWords = f'[{wakeWordStr},{baitWordsStr},{muteCommandsStr}]'


# import vosk model
model = Model(voskModelPath)

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