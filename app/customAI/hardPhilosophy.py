from g4f.client import Client

client = Client()

def hardPhilosophy(request):
  try:
    with open('app/customAI/hardPhilosophy.md', 'r', encoding='utf-8') as file:
      content = file.read()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
          {"role": "system", "content": content},
          {"role": "user", "content": request},
        ],
    )
    return response.choices[0].message.content
  except:
    return 'Ошибка'
