import unittest
from unittest.mock import patch, MagicMock
import json
import queue
import time
from threading import Event
import pyaudio
import wave
import threading

wf = wave.open("tests/data/test_audio.wav", 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                input=True)

# Импортируем тестируемые функции
from app.STT import listenAll, listenCommand  

class TestSpeechRecognition(unittest.TestCase):
    @patch("app.STT.listenAll") # Подставляем listenAll мок-объектом
    def test_listen_command(self, mock_listenAll):

        q = queue.Queue()
        condition = Event()

        # listenCommand(q, condition, stream) 
        listenThread = threading.Thread(target=listenCommand, args=(q,condition,stream))
        listenThread.start()
        time.sleep(5)
        condition.set()
        print("condition set")
        listenThread.join()

        # self.assertFalse(q.empty())  # Очередь должна содержать данные
        self.assertEqual(q.get(), "джарвис")  # Проверяем, что слово правильно распозналось
        mock_listenAll.assert_called_once()  # Проверяем, что listenAll был вызван






















    # def test_listen_all(self, mock_recognize, mock_listen):
    #     """Тест функции listenAll - должна добавлять текст в очередь"""
    #     mock_recognize.return_value = "привет мир"
    #     mock_listen.return_value = MagicMock()  # Подменяем аудиофайл-запись

    #     q = queue.Queue()
    #     start_time = time.time()
        
    #     listenAll(start_time, q)

    #     self.assertFalse(q.empty())  # Очередь должна содержать данные
    #     self.assertEqual(q.get(), "привет мир")  # Проверяем, что фраза распозналась правильно



if __name__ == "__main__":
    unittest.main()
