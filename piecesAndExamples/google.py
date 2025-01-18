import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("Распознанный текст:", text)
        except:
            print('ex')

recognize_speech()
