from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time
from g4f.client import Client
import multiprocessing
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

# fix warning
import asyncio
import sys
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def wright(text,log=False):
    print(text)
    if log == False or wrightLog == True:
        with open('output.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n{text}\n")

def checkRequestInFile():
    with open('output.txt', 'rb') as file:  # Открываем файл в бинарном режиме
        file.seek(0, 2)  # Переходим в конец файла
        position = file.tell()  # Определяем текущую позицию
        line = b''
        while position > 0:
            position -= 1
            file.seek(position)  # Переходим к предыдущему символу
            char = file.read(1)
            if char == b'\n' and line:  # Если встречаем конец строки
                break
            line = char + line
        line = line.decode('utf-8')
        for code in codes:
            if line[:len(code)] == code:
                return line[len(code):]
        return False

def loadSound(text):
    mixer.music.unload()
    tts = gTTS(text=text, lang='ru')
    file_name = "output.mp3"
    tts.save(file_name)
    mixer.music.load("output.mp3")

def tts(inpText, inpCommand):
    while True:
        if not inpCommand.empty():
            command = inpCommand.get()
            if command == "stop":
                mixer.music.stop()
        elif not inpText.empty():
            text = inpText.get()
            loadSound(text)
            mixer.music.play()
        else:
            time.sleep(1)


def requestTextAI(request):
    wright(f'request: {request}',log=True)
    # 'gpt-3.5-turbo','gpt-4o' add to second RS
    models = ['gpt-4']
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": ""},
                    {"role": "user", "content": request}
                ],
                web_search = True,
                temperature=0.9,
                max_tokens=100,
            )
            return response.choices[0].message.content
        except:
            wright('Get Response Failed', log=True)
            pass

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

def listenCommand(queue):
    recognizer = KaldiRecognizer(model, 16000, recognitionWords)
    while True:
        data = stream.read(8192,False)
        if recognizer.AcceptWaveform(data): 
            res = json.loads(recognizer.Result())["text"]
            if res in wakeWord:
                  wright('ON')
                #   tts('да')
                  listenAll(time.time(),queue)
                  wright('OFF')
                #   tts('отключаюсь')
            elif res in muteCommands:
                queue.put(res)

def main(queue,outputText,commandToSound):
    while True:
        req = checkRequestInFile()
        if queue.empty() and not req:
            time.sleep(1)
        else:
            res = req if req else queue.get()

            if res not in commands:
                response = requestTextAI(res)
                outputText.put(response)
                wright(response)
            else:
                if res in muteCommands:
                    wright('stop')
                    commandToSound.put('stop')
            


# <- Voice to text ->

# You can change it
muteCommands = ["тихо","хватит","стоп","молчи"] # Commands to stop play sound
wakeWord = ["ви","вай"]                               # Name of assistant 
baitWords = ['винда','виндвос','в','вы','и']    # For more accurate recognition paste words similar wakeWord
waitTime = 7                                    # Time which assistant listen
wrightLog = False                               # Set True if you need more info in output file
codes = ['  !', '    !','\t!']                        # Combinations in txt file to ask AI

# some boring converting
commands = muteCommands
wakeWordStr = ",".join(f'"{item}"' for item in wakeWord)
baitWordsStr = ",".join(f'"{item}"' for item in baitWords)
muteCommandsStr = ",".join(f'"{item}"' for item in muteCommands)
recognitionWords = f'[{wakeWordStr},{baitWordsStr},{muteCommandsStr}]'

# import vosk model
model = Model(r'C:/work/AI/vosk-model-small-ru-0.22')

# audio stream settings 
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16384)
stream.start_stream()

# text AIs
client = Client()

# sound init 
mixer.init(frequency=53040) # the sound seems to have changed

# run threads
if __name__ == "__main__":
    queue = multiprocessing.Queue()
    outputText = multiprocessing.Queue()
    commandToSound = multiprocessing.Queue()

    listenProcess = multiprocessing.Process(target=listenCommand, args=(queue,))
    mainProcess = multiprocessing.Process(target=main, args=(queue,outputText,commandToSound,))
    ttsProcess = multiprocessing.Process(target=tts, args=(outputText,commandToSound,))

    listenProcess.start()
    mainProcess.start()
    ttsProcess.start()
