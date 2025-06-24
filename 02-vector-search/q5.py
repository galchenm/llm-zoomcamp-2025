from fastembed.embedding import TextEmbedding

model = TextEmbedding(model_name="BAAI/bge-small-en", cache_dir="./.cache", threads=4)

text = "I just discovered the course. Can I join now?"
embedding = next(model.embed([text]))
print(len(embedding)) 
