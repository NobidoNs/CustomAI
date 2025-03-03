from g4f.client import Client
from app.public.wright import wright
from app.public.content import save_context, load_context
from config import MAX_CONTEXT_LENGTH

client = Client()

def requestTextAI(request, fastMode=False, precise=False):
    context = load_context()
    wright(f'request: {request}',log=True)
    wright('*Loading...*')
    models = ['gpt-4o','gpt-4']
    content=''
    if fastMode == True:
        models = ['gpt-4o','gpt-4',]
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
                web_search = True,
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