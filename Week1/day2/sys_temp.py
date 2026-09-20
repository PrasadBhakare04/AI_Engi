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

# prompt = "which"

message = {
    "role" : "user",
    "content" : "give me name for my hotel"
}

#Role is manager change the content to change the role
message_system = {
    "role" : "system",
    # "content" : "You are a strict human officer who also happens to be my manager"
    # "content" : "you are my girlfriend"
    "content" : "You are a name suggesting person"
}

messages = [message_system, message]

#Change the temperature to get more creative answers
#Keep it low when making model for a doctor and high when making for a story writer
response = client.chat.completions.create(model = model, messages=messages, temperature=0)

print(response.choices[0].message.content)