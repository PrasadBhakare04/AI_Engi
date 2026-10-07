import os
from groq import Groq
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()
my_api_key = os.getenv("groq_api")
if not my_api_key:
    raise ValueError("Api key not found")

llm = "openai/gpt-oss-safeguard-20b"
client = Groq(api_key=my_api_key)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(a ,b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

document = [
    "you are going to work in PB Tech Pvt. Ltd."
    "Employees receive 24 days of paid leave per year.",
    "Employees work from the office on Tuesday, Wednesday and Thursday.",
    "Employees receive Rs.3000 per month for gym reimbursement.",
    "Employees can claim Rs.2000 per month for home internet.",
    "Employees have a 90 days notice period." 
]

query = "How many days can i work from home ?"

document_embeddings = embedding_model.encode(document)
query_embedding = embedding_model.encode(query)

def retrieve(query_embedding, document_embeddings):
    scores = []

    for i, document_embedding in enumerate(document_embeddings):
        score = cosine_similarity(query_embedding, document_embedding)
        scores.append((score, document[i]))

    scores.sort(reverse=True)
    return scores[0]

score,context = retrieve(query_embedding, document_embeddings)
print ("this is the score and context ",score, context)

def ask_llm(question, context):
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

    response = client.chat.completions.create(model=llm, messages=messages)

    answer = response.choices[0].message.content
    return answer

print(ask_llm(query, context))