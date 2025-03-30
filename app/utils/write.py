import json

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    outputFile = devolp_config['outputFile']
    writeLog = devolp_config['writeLog']

def write(text,log=False, say=False):
    print(text)
    if log == True or writeLog == True or say:
        with open(outputFile, 'a', encoding='utf-8') as file:
            file.write(f"\n{text}\n")
    if say:
        say.put(text)

