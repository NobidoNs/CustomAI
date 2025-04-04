from g4f.client import Client

client = Client()

def yoda(request):
  try:
    with open('app/customAI/yoda/yoda.md', 'r', encoding='utf-8') as file:
      content = file.read()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
          {"role": "user", "content": f"{content}"},
          {"role": "user", "content": f"{request}"}
        ],
    )
    return response.choices[0].message.content
  except:
    return 'Ошибка'
