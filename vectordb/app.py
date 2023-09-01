import os
from dotenv import load_dotenv
import pinecone
from sentence_transformers import SentenceTransformer
import torch

load_dotenv()

pinecone_key = os.getenv("PINECONE_KEY")
pinecone_env = os.getenv("PINECONE_ENV")

pinecone.init(api_key=pinecone_key, environment=pinecone_env) 

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
query = 'which city is the most populated in the world?'
xq = model.encode(query)

data = [
    {"text": "What is the capital of France?", "category": "LOC"},
    {"text": "Who wrote Hamlet?", "category": "HUM"},
    {"text": "How many planets are there in the solar system?", "category": "NUM"},
    {"text": "What does AIDS stand for?", "category": "ABBR"},
    {"text": "What is the largest animal in the world?", "category": "ENTY"}
]

i = 0
vectors = []
for v in data:
    i+=1
    xq = model.encode(v["text"])
    vectors.append(("Q"+ str(i), xq.tolist(), v))

# print(xq)
# print(vectors)
# exit(1)
if 'test' not in pinecone.list_indexes():
    pinecone.create_index('test',dimension=len(xq.tolist()),metric="cosine")

# connect to index
index = pinecone.Index('test')

index.upsert(
    vectors=vectors,
)

question = "What is the name of Shakespeare's wife?"
xq =  model.encode(question).tolist()
res = index.query(xq, top_k=3,  include_metadata=True)

# Print results
for result in res['matches']:
    print(f"{round(result['score'], 2)}: {result['metadata']['text']} - category {result['metadata']['category']}")