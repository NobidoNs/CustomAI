from g4f.client import Client
from app.utils.write import write
from app.utils.content import save_context, load_context
from app.customAI.philosophy.hardPhilosophy import hardPhilosophy
from app.customAI.coder import getCoderMessage
from app.customAI.default import defaultAI
from app.customAI.jarvis.jarvis import jarvis
from app.customAI.yoda.yoda import yoda
from app.customAI.simple.simple import chars
import json

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    MAX_CONTEXT_LENGTH = config['MAX_CONTEXT_LENGTH']

with open('app/customAI/simple/characters.json', 'r', encoding='utf-8') as file:
    characters = json.load(file).keys()

client = Client()

def requestTextAI(request, branch, chat, web_search): 
    write(f'request: {request}')
    write('*Loading...*', log=True)

    content = ''
    context = load_context(branch, chat)

    messages = [{"role": "system", "content": content}]
    for msg in context[-MAX_CONTEXT_LENGTH:]:
        messages.append(msg) 
    messages.append({"role": "user", "content": request})
    if branch == 'code_editing':
        messages = getCoderMessage(messages[:-1], request)
    elif branch == 'философ':
        response_text = hardPhilosophy(messages)    
    elif branch == 'джарвис':
        response_text = jarvis(messages, web_search)
    elif branch == 'fun':
        if chat == 'мастер йода':
            response_text = yoda(messages)
        elif chat in characters:
            response_text = chars(request, chat)


    try:
        response_text
    except:
        response_text = defaultAI(messages, web_search)

    context.append({
        "role": "user",
        "content": request,
    })
    context.append({
        "role": "assistant",
        "content": response_text
    })
    save_context(context, branch, chat)

    return response_text
