from g4f.client import Client
from app.utils.wright import wright

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    models = devolp_config['AImodelsPriority']

client = Client()

def defaultAI(messages):
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                web_search=False,
                temperature=0.7,
            )
            response_text = response.choices[0].message.content   

            return response_text
        except:
            wright('Ошибка получения ответа', log=True)
            pass
    return ''
