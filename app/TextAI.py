from g4f.client import Client
from app.utils.wright import wright
from app.utils.content import save_context, load_context
from app.customAI.hardPhilosophy import hardPhilosophy
from app.customAI.coder import getCoderMessage
from app.customAI.default import defaultAI
import json

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    MAX_CONTEXT_LENGTH = config['MAX_CONTEXT_LENGTH']

client = Client()

def requestTextAI(request, branch, chat, fastMode=False, precise=False): 
    wright(f'request: {request}', log=True)
    wright('*Loading...*')

    content = ''
    
    if fastMode:
        models = ["gpt-4o-mini", "gemini-1.5-flash"]
    if precise:
        content = 'точный компьютер, который отвечает только по делу'

    context = load_context(branch, chat)

    messages = [{"role": "system", "content": content}]
    for msg in context[-MAX_CONTEXT_LENGTH:]:
        messages.append(msg) 
    
    messages.append({"role": "user", "content": request})

    if branch == 'code_editing':
        messages = getCoderMessage(messages[:-1], request)
    elif branch == 'философ':
        response_text = hardPhilosophy(messages)    
        print(response_text)

    try:
        wright('custom', log=True)
        response_text
    except:
        wright('default', log=True)
        response_text = defaultAI(messages)

    context.append({
        "user": request,
        "assistant": response_text
    })
    save_context(context, branch)

    return response_text
