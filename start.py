import queue
import threading
from app.STT import listenCommand
from app.main import main
from app.TTS import tts

# to run start sound
# try:
#     mixer.music.load(soundStart)
#     mixer.music.play()
# except:
#     pass


if __name__ == "__main__":
    myQueue = queue.Queue()
    outputText = queue.Queue()
    commandToSound = queue.Queue()

    listenThread = threading.Thread(target=listenCommand, args=(myQueue,))
    mainThread = threading.Thread(target=main, args=(myQueue, outputText, commandToSound,))
    ttsThread = threading.Thread(target=tts, args=(outputText, commandToSound,))

    listenThread.start()
    mainThread.start()
    ttsThread.start()

    mainThread.join()
