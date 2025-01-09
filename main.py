from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time
from g4f.client import Client
import multiprocessing
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer

def tts(text):

    tts = gTTS(text=text, lang='ru')
    file_name = "output.mp3"
    tts.save(file_name)
    mixer.init()
    sound = mixer.Sound("C:/work/git/CustomAI/output.mp3")
    sound.play()


def requestTextAI(request):
    print('request:',request)
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
            print('ex')
            pass

def listenAll(startTime,queue):
    googleRec = sr.Recognizer()
    while time.time()-startTime<7:
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
            if res == 'ви':
                  print('ON')
                  listenAll(time.time(),queue)
                  print('OFF')

def main(queue):
    while True:
        if queue.empty():
            time.sleep(1)
        else:
            res = queue.get()
            if res not in hotWords:
                response = requestTextAI(res)
                print(response)
                tts(response)
            


# voice to text
hotWords = ["ви"]
wakeWord = "ви"
baitWords = ['винда','виндвос','в','вы','и']
baitWords = ",".join(f'"{item}"' for item in baitWords)

recognitionWords = f'["{wakeWord}",{baitWords}]'

model = Model(r'C:/work/AI/vosk-model-small-ru-0.22')

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16384)
stream.start_stream()

# text AI
client = Client()


if __name__ == "__main__":
    tts('привет')
    tts('hello')
    
    queue = multiprocessing.Queue()
    outputText = multiprocessing.Queue()

    listenProcess = multiprocessing.Process(target=listenCommand, args=(queue,))
    mainProcess = multiprocessing.Process(target=main, args=(queue,))

    listenProcess.start()
    mainProcess.start()

