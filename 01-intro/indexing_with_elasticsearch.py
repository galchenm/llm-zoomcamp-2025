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

