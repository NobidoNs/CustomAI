from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time
import numpy as np

def amplify_audio(audio_data, factor=5.0):  # Увеличение громкости в 2 раза
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
    audio_np *= factor
    audio_np = np.clip(audio_np, -32768, 32767).astype(np.int16)  # Обрезаем пики
    return audio_np.tobytes()

def is_speech(audio_data):
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    volume = np.abs(audio_np).mean()
    return volume > 300

model = Model('./vosk-model-small-ru-0.22')
recognizer = KaldiRecognizer(model, 16000, '["джарвис", "вь", "в", "вью", "вю", "д", "ж", "дж", "жа", "джа", "жар", "раз", "войс", "результаты", "быстро", "вис", "жара", "дарвин", "арт", "джаз", "жарт", "вирт", "резус", "быстров", "жарко", "войска"]')


audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
stream.start_stream()

while True:
    # data = stream.read(4096, exception_on_overflow=False)
    data = amplify_audio(stream.read(4096, exception_on_overflow=False))
    if is_speech(data):  # Проверяем шум
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            if "text" in result:
                print(result["text"])
            if "text" in result and (result["text"] == "джарвис" or result["text"] == "джавис"):
                print("✅ Активационная фраза 'Джарвис' найдена!")
                print(time.time()-start)
        else:
            partial_result = json.loads(recognizer.PartialResult())
            # print(partial_result)
            if "partial" in partial_result and (partial_result["partial"] == "джарвис" or partial_result["partial"] == "джавис"):
                print("✅ (БЫСТРО) Джарвис распознан частично!")
                start = time.time()

