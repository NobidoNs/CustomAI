from g4f.client import Client
from app.utils.wright import wright

client = Client()

models = ["gpt-4", "phi-4", "llama-3.3-70b", "gemini-1.5-flash", "gpt-4o"]
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