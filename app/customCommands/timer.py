import time
import json

from app.utils.playSound import playSound

with open('devolp_config.json', 'r') as file:
    devolp_config = json.load(file)
    timerSound = devolp_config['timerSound']

def timer(seconds, stop):
  start_time = time.time()
  while not stop.is_set():
    elapsed_time = time.time() - start_time
    if elapsed_time >= seconds:
      playSound(timerSound)
    time.sleep(1)
