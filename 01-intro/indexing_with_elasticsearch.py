import requests

docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']
    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

from elasticsearch import Elasticsearch

# Connect to local Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Define mapping
mapping = {
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"}  # Make course a keyword
        }
    }
}

# Create index
index_name = "course-faq"
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)

# Index documents
for i, doc in enumerate(documents):
    es.index(index=index_name, id=i, document=doc)

# Check one document
count = es.count(index=index_name)
print("Total documents:", count['count'])

#Q3
query = {
    "multi_match": {
        "query": "How do execute a command on a Kubernetes pod?",
        "fields": ["question^4", "text"],
        "type": "best_fields"
    }
}

response = es.search(index=index_name, query=query)
print(response["hits"]["hits"][0]["_score"])

#Q4
query = {
    "bool": {
        "must": {
            "multi_match": {
                "query": "How do copy a file to a Docker container?",
                "fields": ["question^4", "text"],
                "type": "best_fields"
            }
        },
        "filter": {
            "term": {
                "course": "machine-learning-zoomcamp"
            }
        }
    }
}

response = es.search(index=index_name, query=query, size=3)

for i, hit in enumerate(response["hits"]["hits"], start=1):
    print(f"{i}. {hit['_source']['question']}")


#Q5

context_template = """
Q: {question}
A: {text}
""".strip()

# Build context from top 3 hits
context_blocks = [
    context_template.format(
        question=hit["_source"]["question"],
        text=hit["_source"]["text"]
    )
    for hit in response["hits"]["hits"]
]

context = "\n\n".join(context_blocks)

# Final prompt
prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

final_prompt = prompt_template.format(
    question="How do copy a file to a Docker container?",
    context=context
)

# Output length
print("Prompt length:", len(final_prompt))


#Q6

import tiktoken

# Use the GPT-4o tokenizer
encoding = tiktoken.encoding_for_model("gpt-4o")

# Tokenize the final prompt string
tokens = encoding.encode(final_prompt)

# Count the tokens
print("Number of tokens:", len(tokens))

#Q7 ungraded

from gpt4all import GPT4All

# Initialize the local GPT4All model
model = GPT4All("gpt4all-lora")

# Generate response using the final prompt
response = model.generate(final_prompt)

# Print the model's response
print(response)