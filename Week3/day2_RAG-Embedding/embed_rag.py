import os
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer

load_dotenv()

my_api_key = os.getenv("groq_api")

if not my_api_key:
    raise ValueError("Api key not found")

model = SentenceTransformer("all-MiniLM-L6-v2")

# embedding = model.encode("hello how are you")
# print(embedding)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

t1 = "Cat is an animal"
t2 = "Vanila is one of the flavour icecream"

e1 = model.encode(t1)
e2 = model.encode(t2)

print(cosine_similarity(e1, e2))