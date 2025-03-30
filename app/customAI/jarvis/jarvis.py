from g4f.client import Client
import json
with open('devolp_config.json', 'r', encoding='utf-8') as file:
  devolp_config = json.load(file)
  models = devolp_config["AImodelsPriority"]



client = Client()

def jarvis(request, web_search):
  with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    voice = config['voice']
  for model in models:
    try:
      new_request = request[-1]["content"]
      request = request[:-1]
      with open('app/customAI/jarvis/jarvis.md', 'r', encoding='utf-8') as file:
        content = file.read()
        request.append({"role": "user", "content": content})
      if voice == 'джарвис':
        request.append({"role": "system", "content": "в этот раз ответь от мужского лица"})
      else:
        request.append({"role": "system", "content": "в этот раз ответь от женского лица"})
      request.append({"role": "user", "content": new_request})
      response = client.chat.completions.create(
          model=model,
          messages=request,
          web_search=web_search,
          Temperature=0.7,
      )
      response = response.choices[0].message.content

      if web_search:
        index = response.find('[')
        if index != -1:
          response = response[:index]

      return response
    except:
      return 'Ошибка'
  return ''