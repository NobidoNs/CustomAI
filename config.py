import json

with open('devolp_config.json', 'r', encoding='utf-8') as file:
  devolp_config = json.load(file)
  commands = devolp_config["commands"]

allCommands=[]
for group in commands.values():
    for command in group:
        allCommands.append(command)