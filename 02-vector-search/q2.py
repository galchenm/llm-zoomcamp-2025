from fastembed.embedding import TextEmbedding
import numpy as np

# Load the model
embedder = TextEmbedding(model_name="jinaai/jina-embeddings-v2-small-en")

# Embed the query
query = "I just discovered the course. Can I join now?"
query_vector = next(embedder.embed([query]))

doc = "Can I still join the course after the start date?"

# Embed the document
doc_vector = next(embedder.embed([doc]))

# Cosine similarity (dot product, since vectors are normalized)
similarity = np.dot(query_vector, doc_vector)

print("Cosine similarity:", similarity)
