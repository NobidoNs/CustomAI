from g4f.client import Client

client = Client()
models=["gpt-4","gpt-4o","gpt-4o-mini","o1","phi-4","llama-3.3-70b","gemini-1.5-flash"]
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a jarvis from iron man films"},
        {"role": "user", "content": "расскажи анекдот"}
    ],
    # web_search = True,
    temperature=0.7,
)
# print(response.choices[0].message.content)
print(response)