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


import json
with open('downloaded_faq.json', 'w') as file:
    json.dump(documents, file)


from minsearch import Index


# Create and fit the index
index = Index(
    text_fields=["question", "text", "section"],
    keyword_fields=["course"]
)
index.fit(documents)
