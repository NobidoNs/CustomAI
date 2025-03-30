from pygame import mixer
from app.utils.write import write

def playSound(sound):
    try:
        mixer.music.load(sound)
        mixer.music.play(loops=-1)
    except Exception as e:
        write(f"Error loading sound: {e}")
  
def stopSound():
    mixer.music.stop()  # Останавливает воспроизведение