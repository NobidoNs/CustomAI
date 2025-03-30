from g4f.client import Client
import json
with open('devolp_config.json', 'r', encoding='utf-8') as file:
  devolp_config = json.load(file)
  models = devolp_config["AImodelsPriority"]

client = Client()

def hardPhilosophy(request):
  with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    voice = config['voice']
  for model in models:
    try:
      with open('app/customAI/philosophy/hardPhilosophy.md', 'r', encoding='utf-8') as file:
        content = file.read()
      if voice == 'джарвис':
          request.append({"role": "system", "content": "в этот раз ответь от мужского лица"})
      else:
        request.append({"role": "system", "content": "в этот раз ответь от женского лица"})
      response = client.chat.completions.create(
          model=model,
          messages=[
            {"role": "user", "content": f"{content}"},
            {"role": "user", "content": f"{request}"}
          ],
      )
      return response.choices[0].message.content
    except:
      return 'Ошибка'
  return ''
