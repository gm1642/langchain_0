import json
import gradio as gr
import ollama
import chromadb

# Load the data from the JSON file
with open('cleaned_qa_pairs.json', 'r') as f:
    qa_pairs = json.load(f)

client = chromadb.Client()
collection = client.create_collection(name="qa_pairs")

# Prepare a dictionary to store the embeddings
embeddings_dict = {}
#sample question prompt A sum of money is to be distributed among P,Q, R, and S in the proportion 5 : 2 : 4 : 3,respectively.If R gets R 1000 more than S, what is the shareof Q (in Rs)?(a) 500(b) 1000(c) 1500(d) 2000
# Function to add QA pairs to the database and generate embeddings
def add_to_db(qa_pairs):
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

# Function to get a response based on a prompt
def get_response(prompt):
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

    return output['response']

# Add your QA pairs to the database (you might want to do this only once)
add_to_db(qa_pairs)

# Create a Gradio interface
iface = gr.Interface(
    fn=get_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text",
)

if __name__ == "__main__":
    iface.launch()
