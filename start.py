import queue
import threading
from app.STT import listenCommand
from app.main import main
from app.TTS import tts
import time

# to run start sound
# try:
#     mixer.music.load(soundStart)
#     mixer.music.play()
# except:
#     pass

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
        
