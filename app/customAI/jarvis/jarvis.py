from g4f.client import Client

client = Client()

def jarvis(request,web_search):
  try:
    with open('app/customAI/jarvis/jarvis.md', 'r', encoding='utf-8') as file:
      content = file.read()
    request.append({"role": "user", "content": content})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=request,
        web_search=web_search,
        Temperature=0.7,
    )
    return response.choices[0].message.content
  except:
    return 'Ошибка'
