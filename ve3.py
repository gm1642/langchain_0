import ollama
import chromadb

import json
import time

# Load the data from the JSON file
with open('cleaned_qa_pairs.json', 'r') as f:
    qa_pairs = json.load(f)

client = chromadb.Client()
collection = client.create_collection(name="qa_pairs")

# Prepare a dictionary to store the embeddings
embeddings_dict = {}

# Store each question and answer pair in a vector embedding database
for pair in qa_pairs:
    question_id = pair["question_id"]
    question = pair["question"]
    answer = pair["answer"]

    # Concatenate the question and answer
    qa_concat = question + " " + answer

    try:
        # Generate an embedding for the concatenated string
        response = ollama.embeddings(model="mxbai-embed-large", prompt=qa_concat)
        embedding = response["embedding"]

        # Store the embedding in the dictionary
        embeddings_dict[question_id] = embedding

        # Store the embedding in the database
        collection.add(
            ids=[question_id],
            embeddings=[embedding],
            documents=[qa_concat]
        )

        # Wait for 1 second before making the next request
        time.sleep(1)
    except Exception as e:
        print(f"Failed to process question ID {question_id}: {e}")
        print(f"Input prompt: {qa_concat}")
        print("\n")

# Save the embeddings to a JSON file
with open('embeddings.json', 'w') as f:
    json.dump(embeddings_dict, f)