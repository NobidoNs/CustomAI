import json

with open('devolp_config.json', 'r') as file:
    devolp_config = json.load(file)
    outputFile = devolp_config['outputFile']
    wrightLog = devolp_config['wrightLog']

def wright(text,log=False):
    print(text)
    if log == False or wrightLog == True:
        with open(outputFile, 'a', encoding='utf-8') as file:
            file.write(f"\n{text}\n")

