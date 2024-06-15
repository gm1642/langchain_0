import json
import ollama
import chromadb

# Load the data from the JSON file
with open('qa_pairs.json', 'r') as f:
    data = json.load(f)

# Initialize the client and create a collection
client = chromadb.Client()
collection = client.create_collection(name="qa_pairs")

# Store each question-answer pair in a vector embedding database
for item in data:
    question = item['question']
    answer = item['answer']
    qa_pair = f"Question: {question} Answer: {answer}"

    response = ollama.embeddings(model="mxbai-embed-large", prompt=qa_pair)
    embedding = response["embedding"]
    collection.add(
        ids=[item['question_id']],
        embeddings=[embedding],
        documents=[qa_pair]
    )

# an example prompt
prompt = "Consider the circuit shown in the figure. Thecurrent I flowing through the 10 \uf057 resistor is_________."

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