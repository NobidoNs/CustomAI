from g4f.client import Client
from app.utils.wright import wright
from app.utils.content import save_context, load_context
from app.utils.content import load_code_files
import json

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
    MAX_CONTEXT_LENGTH = config['MAX_CONTEXT_LENGTH']

client = Client()

def requestTextAI(request, branch, fastMode=False, precise=False): 
    wright(f'request: {request}', log=True)
    wright('*Loading...*')

    models = ["gpt-4", "phi-4", "llama-3.3-70b", "gemini-1.5-flash", "gpt-4o"]
    content =''
    
    if fastMode:
        models = ["gpt-4o-mini", "gemini-1.5-flash"]
    if precise:
        content = 'точный компьютер, который отвечает только по делу'

    context = load_context(branch)
    if branch == 'code_editing':
        code_context = load_code_files()
        messages = [
            {"role": "system", "content": "Ты опытный программист, анализируй код и помогай с ним. Отвечай на русском"},
            {"role": "system", "content": code_context}
        ]
    else:
        messages = [{"role": "system", "content": content}]
        
    for msg in context[-MAX_CONTEXT_LENGTH:]:
        messages.append({"role": "user", "content": msg["user"]}) 
        messages.append({"role": "assistant", "content": msg["assistant"]})
    messages.append({"role": "user", "content": request})

    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                web_search=False,
                temperature=0.7,
            )
            response_text = response.choices[0].message.content   

            context.append({
                "user": request,
                "assistant": response_text
            })
            save_context(context, branch)

            return response_text
        except:
            wright('Ошибка получения ответа', log=True)
            pass