import json

# Load the data from the JSON file
with open('cleaned_qa_pairs.json', 'r') as f:
    qa_pairs = json.load(f)

# Select the first three question-answer pairs
first_three_pairs = qa_pairs[:3]

# Write the first three pairs to a new JSON file
with open('first_three_pairs.json', 'w') as f:
    json.dump(first_three_pairs, f)