import ollama
import chromadb

import json

# Load the data from the JSON file
with open('cleaned_qa_pairs.json', 'r') as f:
    qa_pairs = json.load(f)

client = chromadb.Client()
collection = client.create_collection(name="qa_pairs")

# Store each question and answer pair in a vector embedding database
for pair in qa_pairs:
    question_id = pair["question_id"]
    question = pair["question"]
    answer = pair["answer"]

    # Concatenate the question and answer
    qa_concat = question + " " + answer

    # Generate an embedding for the concatenated string
    response = ollama.embeddings(model="mxbai-embed-large", prompt=qa_concat)
    embedding = response["embedding"]

    # Store the embedding in the database
    collection.add(
        ids=[question_id],
        embeddings=[embedding],
        documents=[qa_concat]
    )

