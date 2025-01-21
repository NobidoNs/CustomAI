from gtts import gTTS
from pydub import AudioSegment
print("Привет, я твой голосовой помощник!")
# Создаем аудиофайл с помощью gtts
text = "Привет, как дела?"
tts = gTTS(text=text, lang='ru')
tts.save("output.mp3")

audio = AudioSegment.from_file("output.mp3")
new_audio = audio.speedup(playback_speed=1.5)
new_audio.export("output_fast.mp3", format="mp3")