import os
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer



#Qdrant imports-----------------------------------------------------------
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

my_groq_api = os.getenv("groq_api")
model = "openai/gpt-oss-safeguard-20b"

qdrant_api = os.getenv("qdrant_api")
qdrant_url = os.getenv("qdrant_cluster_endpoint")

qdrant_client = QdrantClient(
    url = qdrant_url,
    api_key = qdrant_api
)



#defining parameter of the collection inside vector database--------------------------------------
collection_name = "Knowledgebase"
embedding_size = 384



#Delete if collection exists----------------------------------------------------
if qdrant_client.collection_exists(collection_name):
    print(f"deleting existing collection : {collection_name}")
    qdrant_client.delete_collection(collection_name)



#create collection-----------------------------------------------------------
qdrant_client.create_collection(
    collection_name = collection_name,
    vectors_config=VectorParams(
        size = embedding_size,
        distance = Distance.COSINE     #COSINE is an algorithm for calculating similarity there are multiple algos like difference etc
    ),
)

print(f"created collection: {collection_name}")
print(f"vector size: {embedding_size}")
print(f"Distance: COSINE")


#load the knowledge from a file
document = []
with open("knowledge.txt", "r") as f:
    for line in f:
        if line:
            line = line.strip()
            document.append(line)
print(f"loaded {len(document)} lines in document")


#Creating embeddings------------------------------------------------------------------------------------------- 
print("loading embedding model")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("loaded embedding model")

embeddings = embedding_model.encode(document)
print(f"generated {len(document)} embeddings")
print(f"embedding size: {len(embeddings[0])}")


#creating points---------------------------------------------------------------------------------------------
points = []
for i, embedding in enumerate(embeddings):
    point = PointStruct(
        id = i + 1, 
        vector = embedding.tolist(),
        payload = {
            "text" : document[i]
        }
    )
    points.append(point)


#upload points to Qdrant------------------------------------------------------------------------------------
#upsert = upload + insert, if present don't do anything if not insert
qdrant_client.upsert(
    collection_name = collection_name,
    points = points
)
print(f"uploaded {len(points)} documents to qdrant")



#Search Qdrant----------------------------------------------------------------------------------------------
#top_k = top che kiti lines pahijet(point)
def search(query, top_k = 3):
    #Convert the question into a vector
    query_vector = embedding_model.encode(query).tolist()

    #Search Qdrant for similar vectors
    results = qdrant_client.query_points(
        collection_name = collection_name,
        query = query_vector,
        limit = top_k,
        with_payload = True,
    ).points

    return results



#Test search----------------------------------------------------------------------------------------------------
query = "How many vacation days do I get ?"

results = search(query, 3)

print("\n Search results:")

for result in results:
    print(f"Score: {result.score:.3f}")
    print(result.payload["text"])
    print()



#Connect to Groq and LLM call
groq_client = Groq(api_key=my_groq_api)

def ask_llm(question, context):
    prompt = f"""answer in one line only. Answer only based on this context, do not hallucinate. Context : {context}
    Question : {question}

    if the answer is not present in the context, say:
    "I don't know based on the provided information"
    """
    response = groq_client.chat.completions.create(model= model, messages=[
        {
            "role" : "user",
            "content" : prompt
        }
    ])

    result = response.choices[0].message.content
    return result


#complete RAG pipeline---------------------------------------------------------------------------------------------------
question = "How many vacation days do I get ?"
results = search(question, 3)

#extract text from search result--------------------------------------------------------------------------------------
context = "\n".join(
    result.payload["text"]
    for result in results
)

answer = ask_llm(question, context)
print(f"\n final answer")
print(answer)