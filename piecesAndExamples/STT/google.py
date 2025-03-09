import speech_recognition as sr
import time

recognizer = sr.Recognizer()
def recognize_speech():
    while True:
        start = time.time()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            print(time.time() - start)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("Распознанный текст:", text)
        except:
            print('ex')

recognize_speech()
