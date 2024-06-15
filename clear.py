import json
import time
import ollama
import chromadb
client = chromadb.Client()
client.delete_collection(name="qa_pairs")