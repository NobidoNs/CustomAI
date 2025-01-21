from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "точный компьютер, который отвечает только по делу"},
        {"role": "user", "content": "1+1"}
    ],
    web_search = True,
    temperature=0,
)

print(response.choices[0].message.content)