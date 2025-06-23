from fastembed.embedding import TextEmbedding
import numpy as np

# Load the model
embedder = TextEmbedding(model_name="jinaai/jina-embeddings-v2-small-en")

# Embed the query
query = "I just discovered the course. Can I join now?"
query_vector = next(embedder.embed([query]))

# Check shape and min value
print("Vector shape:", query_vector.shape)
print("Min value:", query_vector.min())
