from vosk import Model, KaldiRecognizer
import pyaudio
import json

model = Model(r'C:/work/AI/vosk-model-small-ru-0.22')


# hotwords= '["ви"]'
# recognizer = KaldiRecognizer(model, 16000, hotwords)

recognizer = KaldiRecognizer(model, 16000)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
  data = stream.read(4096)
  if recognizer.AcceptWaveform(data):
    print(recognizer.Result())