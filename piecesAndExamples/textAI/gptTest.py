from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a jarvis from iron man films"},
        {"role": "user", "content": "расскажи анекдот"}
    ],
    web_search = True,
    temperature=0.7,
)
print(response.choices[0].message.content)