#This is the first iteration of RAG

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

my_api_key = os.getenv("groq_api")

if not my_api_key:
    raise ValueError("Api key not found")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-safeguard-20b"

#step 1 : creating knowledge base
knowledge_base = {
    "age" : "21 years old",
    "background" : "comes from a village called Ahilyanagar",
    "education" : "he is an IT engineer"
}

#step 2 : retrival
def retrieve_info(question) :
    question = question.lower()

    if "age" in question:
        return knowledge_base["age"]

    elif "background" in question:
        return knowledge_base["background"]

    elif "prasad" in question:
        return knowledge_base

    else :
        return None

def ask_llm(question):
    context = retrieve_info(question)
    sys_prompt = f"""answer in one line only. Answer only based on this context, do not hallucinate. Context : {context}"""

    system_message = {
        "role" : "system",
        "content" : sys_prompt
    }
    message = {
        "role" : "user",
        "content" :question
    }

    messages = [message, system_message]

    response = client.chat.completions.create(model=model, messages=messages)

    answer = response.choices[0].message.content
    return answer

question = "prasad"

print(ask_llm(question))