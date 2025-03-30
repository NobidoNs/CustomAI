import queue
import threading
import time
import json
import sys
from pygame import mixer
from app.init import run_init
from app.utils.write import write
from app.STT import listenCommand, makeStream
from app.main import main
from app.TTS import tts
import asyncio

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    soundStart = config['soundStart']

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    init = devolp_config['init']

if not init:
    run_init()


condition = threading.Event()
if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    myQueue = queue.Queue()
    outputText = queue.Queue()
    commandToSound = queue.Queue()

    stream = makeStream()

    listenThread = threading.Thread(target=listenCommand, args=(myQueue,condition,stream,outputText))
    mainThread = threading.Thread(target=main, args=(myQueue, outputText, commandToSound,condition))
    ttsThread = threading.Thread(target=tts, args=(outputText, commandToSound,condition))

    listenThread.start()
    mainThread.start()
    ttsThread.start()

    # to run start sound
    if soundStart:
        try:
            mixer.music.load(soundStart)
            mixer.music.play()
        except:
            write("Error loading soundStart")

    try:
        while not condition.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        condition.set()
        
