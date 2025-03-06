import queue
import threading
import time
import json
from pygame import mixer
from app.utils.wright import wright
from app.STT import listenCommand
from app.main import main
from app.TTS import tts

with open('config.json', 'r') as file:
    config = json.load(file)
    soundStart = config['soundStart']

# to run start sound
if soundStart:
    try:
        mixer.music.load(soundStart)
        mixer.music.play()
    except:
        wright("Error loading soundStart", True)

condition = threading.Event()
if __name__ == "__main__":
    myQueue = queue.Queue()
    outputText = queue.Queue()
    commandToSound = queue.Queue()

    listenThread = threading.Thread(target=listenCommand, args=(myQueue,condition))
    mainThread = threading.Thread(target=main, args=(myQueue, outputText, commandToSound,condition))
    ttsThread = threading.Thread(target=tts, args=(outputText, commandToSound,condition))

    listenThread.start()
    mainThread.start()
    ttsThread.start()

    try:
        while not condition.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        condition.set()
        
