from pygame import mixer
from app.utils.wright import wright

def playSound(sound):
    try:
        mixer.music.load(sound)
        mixer.music.play(loops=-1)
    except Exception as e:
        wright(f"Error loading sound: {e}")
  
def stopSound():
    mixer.music.stop()  # Останавливает воспроизведение