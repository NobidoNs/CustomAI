import asyncio
import edge_tts

async def text_to_speech():
    #with open("test.txt", "r", encoding="utf-8") as file:
    #    text = file.read()
    text = "Спасибо, у меня всё отлично! 😊 А у вас как дела?"
    # Создаем объект TTS и записываем в MP3
    tts = edge_tts.Communicate(text, "ru-RU-DmitryNeural")
    await tts.save("output.mp3")

    print("Файл 'output.mp3' успешно создан!")

# Запуск асинхронной функции
asyncio.run(text_to_speech())
