from pygame import mixer
from app.utils.wright import wright

def playSound(sound):
    try:
        mixer.music.load(sound)
        mixer.music.play()
    except:
        wright("Error loading sound")