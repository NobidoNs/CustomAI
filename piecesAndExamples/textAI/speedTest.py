from g4f.client import Client
import time
import random

client = Client()
total_time = 0
requests = 5
# "gpt-4",
print(f"Running {requests} test requests...")
models=["phi-4","llama-3.3-70b","gemini-1.5-flash","gpt-4o","gpt-4o-mini","o1",]
for model in models:
    for i in range(requests):
        time.sleep(6*random.random())
        start_time = time.time()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "точный компьютер, который отвечает только по делу"},
                {"role": "user", "content": random.randint(1,100)}
            ],
            # web_search = True,
            temperature=0,
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        total_time += response_time
        
        # print(f"Request {i+1}:")
        # print(f"Response: {response.choices[0].message.content}")
        print(f"Time: {response_time:.2f} seconds\n")

    average_time = total_time / requests
    # print(f"Response: {response.choices[0].message.content}")
    print(f"Average response time: {average_time:.2f} seconds for model {model}")
    average_time = 0
    total_time = 0

