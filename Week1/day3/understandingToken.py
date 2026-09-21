import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("groq_api")

if not my_api_key:
    raise ValueError("Api key not found")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"

#Three prompts
prompt1 = "Hi"
prompt2 = "Explain time travel in detail"
prompt3 = "write a 1000 word essay on machine learning"

prompts = [prompt1, prompt2, prompt3]

#Didn't work
system_message = {
    "role" : "system",
    "content" : "don't use more than 100 tokens while generating response"
}

for prompt in prompts :
    message = {
        "role" : "user",
        "content" : prompt
    }

    messages = [message]   
    response = client.chat.completions.create(model = model, messages=messages)
    usage = response.usage
    print(f"Prompt: {prompt} --> your tokens: {usage.prompt_tokens} completion_tokens: {usage.completion_tokens}")
    print(f"Finish Reason: {response.choices[0].finish_reason}")
    # print(response.choices[0].message.content)