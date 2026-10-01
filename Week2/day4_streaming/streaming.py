import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

my_api_key = os.getenv("groq_api")

if not my_api_key:
    raise ValueError("Api key not set")

client = Groq(api_key = my_api_key)

message = {
    "role":"user",
    "content":"generate a summary of the web series Breaking Bad all seasons dont use table give me paragraphs"
}

messages = [message]

# response = client.chat.completions.create(model = "openai/gpt-oss-20b", messages = messages)
# answer = response.choices[0].message.content
# print(answer)


stream = client.chat.completions.create(model = "openai/gpt-oss-20b", messages = messages, stream = True)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)

#flush variable is the delay between chunks
#end = "" end just prints the new chunk on the new line