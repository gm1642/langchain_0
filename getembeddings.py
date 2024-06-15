import json
import ollama
import chromadb
# Get all embeddings from the collection
embeddings = collection.get()

# Print each embedding
for embedding in embeddings:
    print(f"ID: {embedding['id']}")
    print(f"Embedding: {embedding['embedding']}")
    print(f"Document: {embedding['document']}")
    print()