import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("groq_api")

client = Groq(api_key = my_api_key)
model = "openai/gpt-oss-120b"

prompt = """
#ROLE
You are a support assistant at a mobile/laptop company
#TASK
You have fully understand the meaning and intent behind the issue then classify that in a category
#CONSTRAINT
You have to classify th issue in one of three categories namely billing, technical, return.
#OUTPUT FORMAT
Your answer should be in one word only. The one word should be one of the categories mentioned in the constraint
#EXAMPLES
For and instance if a user complain says that he wants a refund then the category is Return
if the user issues states that the user don't want their product then also the category is Return

#FALLBACK
If the issue is unrelated to any of the categories mentioned in constrinats, then the answer should be OTHER

This is the complaint:
my laptop is not working, it says drivers not found and i don't want my laptop
"""
message = {
    "role":"user",
    "content":prompt
}

messages = [message]


response = client.chat.completions.create(messages = messages, model = model)

print(response.choices[0].message.content)