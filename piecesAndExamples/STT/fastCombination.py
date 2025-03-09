from vosk import Model, KaldiRecognizer
import pyaudio
import json
import numpy as np
import collections
import speech_recognition as sr
import time
import threading

# Настройки
SAMPLE_RATE = 16000
BUFFER_SIZE = 4096
AUDIO_DURATION = 2  # В секундах
MAX_FRAMES = (SAMPLE_RATE // BUFFER_SIZE) * AUDIO_DURATION

def amplify_audio(audio_data, factor=5.0):
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
    audio_np *= factor
    audio_np = np.clip(audio_np, -32768, 32767).astype(np.int16)
    return audio_np.tobytes()

def is_speech(audio_data):
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    volume = np.abs(audio_np).mean()
    return volume > 300

def recognize_speech_buffer(audio_buffer):
    global googleRec

    audio_data = b''.join(audio_buffer)

    audio_data = sr.AudioData(audio_data, SAMPLE_RATE, 2)

    try:
        text = googleRec.recognize_google(audio_data, language="ru-RU")
        print("🎤 Распознанный текст:", text)
    except sr.UnknownValueError:
        print("❌ Google Speech не распознал речь")
    except sr.RequestError:
        print("⚠️ Ошибка запроса к Google Speech API")

model = Model('./vosk-model-small-ru-0.22')
recognizer = KaldiRecognizer(model, 16000, '["джарвис", "вь", "в", "вью", "вю", "д", "ж", "дж", "жа", "джа", "жар", "раз", "войс", "результаты", "быстро", "вис", "жара", "дарвин", "арт", "джаз", "жарт", "вирт", "резус", "быстров", "жарко", "войска"]')

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=BUFFER_SIZE)
stream.start_stream()

audio_buffer = collections.deque(maxlen=MAX_FRAMES)

googleRec = sr.Recognizer()
is_recognized = False

def process_audio():
    global is_recognized
    while True:
        data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
        data = amplify_audio(data)
        audio_buffer.append(data)

        if is_speech(data):
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                # print("✅ Распознанная фраза:", result.get("text", ""))
            else:
                partial_result = json.loads(recognizer.PartialResult())
                partial_text = partial_result.get("partial", "")
                
                if "джарвис" in partial_text.lower() and not is_recognized:
                    is_recognized = True 
                    print("✅ (БЫСТРО) Джарвис распознан частично!")
                    threading.Thread(target=recognize_speech_buffer, args=(list(audio_buffer),), daemon=True).start()
                    is_recognized = False

audio_thread = threading.Thread(target=process_audio, daemon=True)
audio_thread.start()

while True:
    time.sleep(0.1)
