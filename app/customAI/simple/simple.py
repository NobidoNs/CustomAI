from g4f.client import Client
import json

client = Client()

def chars(request, char,web_search):
  try:
    with open('app/customAI/simple/characters.json', 'r', encoding='utf-8') as file:
      characters = json.load(file)

    response = client.chat.completions.create(
        model="gpt-4o",
        web_search=web_search,
        messages=[
          {"role": "system", "content": f"Настройки стилистики Объедини и применей все эти параметры к тексту одновременно: {characters[char]}"},
          {"role": "user", "content": f"{request}"}
        ],
    )
    return response.choices[0].message.content
  except:
    return 'Ошибка'
