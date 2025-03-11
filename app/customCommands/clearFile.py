import json

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    outputFile = devolp_config['outputFile']

def clearFile():
    open(outputFile, 'w', encoding='utf-8')