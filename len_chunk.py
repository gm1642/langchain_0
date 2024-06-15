import json

# Load the JSON data from the file
with open('cleaned_qa_pairs.json', 'r') as file:
    qa_pairs = json.load(file)

# Iterate through each question-answer pair and print the length of each question and answer
for pair in qa_pairs:
    question_length = len(pair['question'])
    answer_length = len(pair['answer'])
    print(f"Question ID: {pair['question_id']}, Question Length: {question_length}, Answer Length: {answer_length}")