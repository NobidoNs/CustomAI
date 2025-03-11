import os
import time
import json

with open('devolp_config.json', 'r', encoding='utf-8') as file:
    devolp_config = json.load(file)
    backupPath = devolp_config['backupPath']
    outputFile = devolp_config['outputFile']

def saveBackup(custom_name=None):
    if not os.path.exists(backupPath):
        os.makedirs(backupPath)
    if custom_name:
        backup_name = f"{backupPath}/{custom_name}.md"
    else:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_name = f"{backupPath}/output_backup_{timestamp}.md"
    
    with open(outputFile, 'r', encoding='utf-8') as source:
        with open(backup_name, 'w', encoding='utf-8') as backup:
            backup.write(source.read())
    return backup_name