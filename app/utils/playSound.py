from pygame import mixer
from app.utils.write import write

def playSound(sound):
    try:
        mixer.music.load(sound)
        mixer.music.play()
    except:
        write("Error loading sound")