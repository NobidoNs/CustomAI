import json
from config import outputFile, wrightLog

def wright(text,log=False):
    print(text)
    if log == False or wrightLog == True:
        with open(outputFile, 'a', encoding='utf-8') as file:
            file.write(f"\n{text}\n")

