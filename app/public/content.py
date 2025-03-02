import json
from config import CONTEXT_FILE

def save_context(context):
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)

def load_context():
    try:
        with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []