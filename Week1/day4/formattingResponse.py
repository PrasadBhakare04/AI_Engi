import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

##pydantic is a library which has methods and classes which helps in data conversion and creating schemas for those types
from pydantic import BaseModel
import json

load_dotenv()
my_api_key = os.getenv("groq_api")

client = Groq(api_key = my_api_key)

#as the Ticket is child of BaseModel class it helps us to convert the variables into a json schema as it has the function
# model_json_schema() this is inherited from BaseModel class
class Ticket(BaseModel):
    name:str
    email:str
    issue:str
    city:str

schema = Ticket.model_json_schema()

response_format = {
    "type":"json_object"
}

system_prompt = f"""
the format should be json
{schema}
"""
system_message ={
    "role": "system",
    "content": system_prompt
}

user_message={
    "role":"user",
    "content":"this is the customer ticket extract personal information from this i am Prasad i have an phone which is not working it is restarting on its own. I live in Maharashtra. my email is abc@gmail.com"
}

messages = [system_message, user_message]

response = client.chat.completions.create(model="openai/gpt-oss-120b", messages = messages)

answer = response.choices[0].message.content
# print(answer)

raw_json = answer
data_file =json.loads(raw_json) #loads is used to process json which comes in string format generally a response from an api and load is used for a json file
ticket=Ticket(**data_file)
print(ticket.name)
print(ticket.email)
print(ticket.issue)
print(ticket.city)
