import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("groq_api")

if not my_api_key:
    raise ValueError("Api key not found")

client = Groq(api_key=my_api_key)

model = "groq/compound"

prompt = "which"

message = {
    "role" : "user",
    "content" : prompt
}

messages = [message]

response = client.chat.completions.create(model = model, messages=messages)

print(response.choices[0].message.content)