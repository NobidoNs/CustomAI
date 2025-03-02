from pygame import mixer
from gtts import gTTS
from pydub import AudioSegment
import time
from app.public.wright import wright
from config import soundStart, AUDIO_FREQUENCY

def loadSound(text,speed=1):
    mixer.music.unload()
    tts = gTTS(text=text, lang='ru')
    file_name = "output.mp3"
    tts.save(file_name)
    if speed != 1:
        audio = AudioSegment.from_file("output.mp3")
        new_audio = audio.speedup(playback_speed=speed)
        new_audio.export("output.mp3", format="mp3")

    mixer.music.load("output.mp3")

def tts(inpText, inpCommand):
    speed = 1
    while True:
        if not inpCommand.empty():
            command = inpCommand.get()
            argument = command.split(' ', 1)[1] if ' ' in command else None
            if command == "stop":
                mixer.music.stop()
            elif command == "-mute":
                break
            elif "-speed" in command:
                if argument == 'up':
                    speed += 0.5
                elif argument == 'down':
                    speed -= 0.5
                else:
                    speed = float(argument)
                wright(f'Speed set to {speed}')
        elif not inpText.empty():
            text = inpText.get()
            for char in "*#`></_-+":
                text = text.replace(char, "")
            loadSound(text,speed=speed)
            mixer.music.play()
        else:
            time.sleep(1)

# sound init 
mixer.init(frequency=AUDIO_FREQUENCY) # the sound seems to have changed
