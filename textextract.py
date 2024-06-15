import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    # Open the PDF file
    document = fitz.open(file_path)
    text = ''
    # Iterate over each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)  # Load each page
        text += page.get_text()  # Extract text from each page
    document.close()
    return text

# Call the function and print the result
file_path = "GATE.pdf"  # Replace with your local PDF file name
extracted_text = extract_text_from_pdf(file_path)
print(extracted_text[:500])  # Print the first 500 characters of the extracted text
