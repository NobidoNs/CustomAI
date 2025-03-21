from g4f.client import Client
from app.utils.content import load_code_files

client = Client()

def getCoderMessage(data):
  try:
    code_context = load_code_files()
    messages = [
            {"role": "system", "content": "Ты опытный программист, анализируй код и помогай с ним. Отвечай на русском"},
            {"role": "system", "content": code_context}
        ]
    return messages + data
  except:
    return 'Ошибка'
