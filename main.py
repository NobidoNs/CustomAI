from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time
from g4f.client import Client
import multiprocessing
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import os
from pydub import AudioSegment
from config import *  # Import all config variables
import json

# fix warning
import asyncio
import sys
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def load_context():
    try:
        with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_context(context):
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)

def save_backup(custom_name=None):
    if not os.path.exists(backupPath):
        os.makedirs(backupPath)
    if custom_name:
        backup_name = f"{backupPath}/{custom_name}.md"
    else:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_name = f"{backupPath}/output_backup_{timestamp}.md"
    
    with open(outputFile, 'r', encoding='utf-8') as source:
        with open(backup_name, 'w', encoding='utf-8') as backup:
            backup.write(source.read())
    return backup_name
def clearFile():
    open(outputFile, 'w', encoding='utf-8')

def wright(text,log=False):
    print(text)
    if log == False or wrightLog == True:
        with open(outputFile, 'a', encoding='utf-8') as file:
            file.write(f"\n{text}\n")

def requestInFile():
    with open(outputFile, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.splitlines()

    for indexLine in range(1,len(lines)+1):
        line = lines[-indexLine]
        for code in codes:
            if code in line:
                return "".join(lines[-indexLine:]).split(code,1)[1]
        if line in stopFind:
            return ''
    return ''

    
def loadSound(text,speed=1):
    mixer.music.unload()
    tts = gTTS(text=text, lang='ru')
    file_name = "output.mp3"
    tts.save(file_name)
    if speed != 1:
        audio = AudioSegment.from_file("output.mp3")
        new_audio = audio.speedup(playback_speed=speed)
        new_audio.export("output.mp3", format="mp3")

    mixer.music.load("output.mp3")

def tts(inpText, inpCommand):
    speed = 1
    while True:
        if not inpCommand.empty():
            command = inpCommand.get()
            argument = command.split(' ', 1)[1] if ' ' in command else None
            if command == "stop":
                mixer.music.stop()
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
            text = inpText.get()
            for char in "*#`></_-+":
                text = text.replace(char, "")
            loadSound(text,speed=speed)
            mixer.music.play()
        else:
            time.sleep(1)


def requestTextAI(request, fastMode=False, precise=False):
    context = load_context()
    wright(f'request: {request}',log=True)
    wright('*Loading...*')
    models = ['gpt-4','gpt-3.5-turbo','gpt-4o']
    content=''
    if fastMode == True:
        models = ['gpt-3.5-turbo','gpt-4o''gpt-4',]
    if precise == True:
        content = 'точный компьютер, который отвечает только по делу'
    
    messages = [{"role": "system", "content": content}]
    # Add context messages
    for msg in context[-MAX_CONTEXT_LENGTH:]:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["assistant"]})
    messages.append({"role": "user", "content": request})

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                web_search = True,
                temperature=0.7,
            )
            response_text = response.choices[0].message.content
            
            # Save new context
            context.append({
                "user": request,
                "assistant": response_text
            })
            save_context(context)
            
            return response_text
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
            elif res in commands['muteCommands']:
                queue.put(res)

def main(queue,outputText,commandToSound):
    while True:
        req = requestInFile()
        if queue.empty() and not req:
            time.sleep(1)
        else:
            if req: 
                res = req
            else:
                res = queue.get()
                wright(res)

            try:
                firstWord = res.split(' ', 1)[0]
                for i in commands:
                    if res in i:
                        firstWord = i
            except:
                firstWord = None
            print(allCommands,firstWord)
            if firstWord in allCommands:
                command = firstWord
                argument = res.split(' ', 1)[1] if ' ' in res else None
                if command in commands['muteCommands']:
                    wright('stop')
                    commandToSound.put('stop')

                elif command in commands['voiceCommands']:
                    wright('MUTE')
                    commandToSound.put('-mute')

                elif command in commands['clearCommands']:
                    clearFile()
                    continue

                elif command in commands['restartZapretCommands']:
                    wright('Restarting zapret program...')
                    # Kill existing process if running
                    os.system(f'taskkill /F /IM {os.path.basename(zapretProcess)}')
                    # Start new instance
                    os.startfile(zapretPath)

                elif command in commands['saveCommands']:
                    backup_file = save_backup(argument)
                    wright(f'Backup saved as: {backup_file}')

                elif command in commands['setSpeedCommands']:
                    commandToSound.put(f'-speed {argument}')

                elif command in commands['upSpeedCommands']:
                    commandToSound.put(f'-speed up')
                elif command in commands['downSpeedCommands']:
                    commandToSound.put(f'-speed down')
                
                elif command in commands['clearContextCommands']:
                    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
                        json.dump([], f)
                    wright('Context cleared')
            else:
                response = requestTextAI(res)
                outputText.put(response)
                wright(response)

            wright('------------')


# some boring converting
wakeWordStr = ",".join(f'"{item}"' for item in wakeWord)
baitWordsStr = ",".join(f'"{item}"' for item in baitWords)
muteCommandsStr = ",".join(f'"{item}"' for item in commands['muteCommands'])
recognitionWords = f'[{wakeWordStr},{baitWordsStr},{muteCommandsStr}]'

allCommands=[]
for group in commands.values():
    for command in group:
        allCommands.append(command)


# import vosk model
model = Model(voskModelPath)

# audio stream settings 
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16384)
stream.start_stream()

# text AIs
client = Client()

# sound init 
mixer.init(frequency=AUDIO_FREQUENCY) # the sound seems to have changed

# to run start sound
try:
    mixer.music.load(soundStart)
    mixer.music.play()
except:
    pass


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

    mainProcess.join()
