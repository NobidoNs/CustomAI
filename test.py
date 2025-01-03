from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time
from g4f.client import Client

def requestTextAI(request):
    models = ['gpt-4o','gpt-4o-mini','gpt-4-turbo','gpt-3.5-turbo']
    for model in models:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Ты искусственный интелеки Джарвис из фильмов про железного человека"},
                {"role": "user", "content": request}
            ],
            web_search = True,
            temperature=0.9,
        )
        return response.choices[0].message.content

def main():
    # voice to text
    recognizer = KaldiRecognizer(model, 16000, hotwords)
    startTime = -1
    while True:
        data = stream.read(16384)
        if recognizer.AcceptWaveform(data):

            res = json.loads(recognizer.Result())["text"]

    # check wake word 
            if res == wakeWord:
                startTime = time.time()
                recognizer = KaldiRecognizer(model, 16000)
                print('activate')
            
    # check wake word duration
            elif startTime != -1 :
                if time.time()-startTime <= 10:
                    if res != '':
                        startTime = time.time()
    # request to textAI
                    print('You say:', res)
                    print(requestTextAI(res))
                else:
                    print('disable')
                    startTime = -1
                    recognizer = KaldiRecognizer(model, 16000, hotwords)

# voice to text
model = Model(r'C:/work/AI/vosk-model-small-ru-0.22')

hotwords= '["джарвис"]'

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=16384)
stream.start_stream()

wakeWord = hotwords[0]

# text AI
client = Client()


if __name__ == "__main__":
    main()