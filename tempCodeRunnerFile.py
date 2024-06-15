# Retrieve the documents and their embeddings
for id in ids:
    doc = collection.get(id, include=["embeddings"])
    print(f"Document ID: {id}")
    print(f"Document Text: {doc['documents']}")
    print(f"Document Embedding: {doc['embeddings']}")
    print("\n")

    # an example prompt
prompt = "What animals are llamas related to?"

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