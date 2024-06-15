import json
import time
import ollama
import chromadb

# Load the data from the JSON file
with open('first_three_pairs.json', 'r') as f:
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

    # Retrieve the stored document and print it
    doc = collection.get(question_id, include=["embeddings"])

    print(f"Question ID: {question_id}")
    print(f"Document Text: {doc['documents']}")
    print(f"Document Embedding: {doc['embeddings']}")
    print("\n")

# # Save the embeddings to a JSON file
# with open('embeddings.json', 'w') as f:
#     json.dump(embeddings_dict, f)
prompt = "A sum of money is to be distributed among P,Q, R, and S in the proportion 5 : 2 : 4 : 3,respectively.If R gets R 1000 more than S, what is the shareof Q (in Rs)"

# generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
  prompt=prompt,
  model="mxbai-embed-large"
)
results = collection.query(
  query_embeddings=[response["embedding"]],
  n_results=1
)
data = results['documents'][0][0]

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama2",
  prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(output['response'])