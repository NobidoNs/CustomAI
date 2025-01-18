import speech_recognition as sr
import multiprocessing

def listenAll(queue):
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            queue.put(audio)
            print("Audio added to queue")

def recognize_speech(queue):
    recognizer = sr.Recognizer()
    while True:
        if not queue.empty():
            audio = queue.get()
            try:
                text = recognizer.recognize_google(audio, language="ru-RU")
                print("Распознанный текст:", text)
            except:
                print('ex')

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    listenAllProcess = multiprocessing.Process(target=listenAll, args=(queue,))
    # recognize_speechProcess = multiprocessing.Process(target=recognize_speech, args=(queue,))
    listenAllProcess.start()
    # recognize_speechProcess.start()
