from gtts import gTTS
from pygame import mixer

mixer.init()

text = 'Привет мир!'
tts = gTTS(text=text, lang='ru')
file_name = "output.mp3"
tts.save(file_name)
mixer.music.load("output.mp3")
mixer.music.play()
input()