from g4f.client import Client
from app.utils.content import load_code_files

client = Client()

def getCoderMessage(messages, request):
  try:
    code_context = load_code_files()
    con = [
            {"role": "system", "content": "Ты опытный программист, анализируй код и помогай с ним. Отвечай на русском"},
            {"role": "system", "content": code_context}
        ]
    req = [{"role": "user", "content": request}]
    return con + messages + req
  except Exception as e:
    print(e)
    return 'Ошибка'
