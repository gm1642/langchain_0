import re
import json

# Open your JSON file
with open('qa_pairs.json') as f:
    data = json.load(f)

# Iterate over each question in your data
for question in data:
    # Remove Unicode characters from the question text
    question['question'] = re.sub(r'\\u[0-9A-Fa-f]+', '', question['question'])
    # Remove Unicode characters from the answer text
    question['answer'] = re.sub(r'\\u[0-9A-Fa-f]+', '', question['answer'])

# Save the cleaned data back to a JSON file
with open('cleaned_qa_pairs.json', 'w') as f:
    json.dump(data, f)