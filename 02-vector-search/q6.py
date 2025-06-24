from fastembed.embedding import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import requests

# 1. Load documents
docs_url = 'https://github.com/alexeygrigorev/llm-rag-workshop/raw/main/notebooks/documents.json'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []
for course in documents_raw:
    if course['course'] != 'machine-learning-zoomcamp':
        continue
    for doc in course['documents']:
        doc['course'] = course['course']
        documents.append(doc)

# 2. Create embedding model
model = TextEmbedding(model_name="BAAI/bge-small-en", cache_dir="./.cache", threads=4)

# 3. Create Qdrant client (localhost or in-memory)
client = QdrantClient(":memory:") 

# 4. Create collection
DIM = 384  # For BAAI/bge-small-en
client.recreate_collection(
    collection_name="ml_faq",
    vectors_config=VectorParams(size=DIM, distance=Distance.COSINE),
)

# 5. Add documents
points = []
for idx, doc in enumerate(documents):
    text = doc['question'] + ' ' + doc['text']
    embedding = next(model.embed([text]))
    points.append(PointStruct(id=idx, vector=embedding, payload=doc))

client.upsert(collection_name="ml_faq", points=points)

# 6. Embed the query
query = 'I just discovered the course. Can I join now?'
query_vector = next(model.embed([query]))

# 7. Search
results = client.search(
    collection_name="ml_faq",
    query_vector=query_vector,
    limit=1,
)

# 8. Top result
top_score = results[0].score
print("Top score:", top_score)
print("Top match:", results[0].payload['question'])
