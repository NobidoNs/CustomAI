import requests
import pygame
import io

url = 'https://apihost.ru/tts.php'

data = {
    "data": [{
        "lang": "ru-RU",
        "speaker": "2001",
        "emotion": "",
        "text": "Озвучка текста нейросетями: Более 1000 голосов, от Детских до знаменитостей, Санта-Клаус, Левитан, Ленин, Бот Максим – Настройка Высоты, Скорости и Интонации для живых и убедительных аудио\n\n",
        "rate": "1.5",
        "pitch": "1.0",
        "type": "wav",
        "pause": "0"
    }]
}

response = requests.post(url, json=data)

if response.status_code == 200:
    audio_url = response.json()['audio']
    response = requests.get(audio_url)
    audio_data = io.BytesIO(response.content)

    # Инициализируем pygame
    pygame.mixer.init()

    # Загружаем аудио из памяти
    pygame.mixer.music.load(audio_data)

    # Воспроизводим аудио
    pygame.mixer.music.play()

    # Ждем, пока аудио закончится
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
else:
    print(response)
