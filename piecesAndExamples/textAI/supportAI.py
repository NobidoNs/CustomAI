from g4f.client import Client
from app.utils.wright import wright
from app.utils.content import save_context, load_context
import json

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    MAX_CONTEXT_LENGTH = config['MAX_CONTEXT_LENGTH']

client = Client()

def requestTextAI(request, fastMode=False, precise=False):
    context = load_context()
    wright(f'request: {request}',log=True)
    wright('*Loading...*')
    # models = ['gpt-4o','gpt-4']
    models = ['gpt-4']
    content=''
    if fastMode == True:
        # models = ['gpt-4o','gpt-4',]
        models = ['gpt-4']
    if precise == True:
        content = 'точный компьютер, который отвечает только по делу'
    
    messages = [{"role": "system", "content": content}]
    # Add context messages
    for msg in context[-MAX_CONTEXT_LENGTH:]:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["assistant"]})
    messages.append({"role": "user", "content": request})

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                web_search = False,
                temperature=0.7,
            )
            response_text = response.choices[0].message.content
            
            # Save new context
            context.append({
                "user": request,
                "assistant": response_text
            })
            save_context(context)
            
            return response_text
        except:
            wright('Get Response Failed', log=True)
            pass