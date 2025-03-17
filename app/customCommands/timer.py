import time
import json
from app.utils.loopSound import playSound, stopSound

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    timerSound = devolp_config['timerSound']

def timer(seconds, stop_event):
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time < seconds):
        time.sleep(1)
    playSound('sounds/timer.mp3')
    while not stop_event.is_set():
        time.sleep(1)
    stopSound()