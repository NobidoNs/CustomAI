from g4f.client import Client

client = Client()

def convertTime(timeToAI):
  try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "ты отвечаешь только одним числомб ничего не пишешь кроме одного числа, если не знаешь ответ, то отвечаешь 0"},
            {"role": "user", "content": f"переведи {timeToAI} в секунды"},
        ],
    )
    return int(response.choices[0].message.content)
  except:
    return 0