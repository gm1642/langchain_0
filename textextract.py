import PyPDF2

def extract_text_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    pdf_file_obj.close()
    return text

# Call the function and print the result
file_path = r"C:\Users\samkh\Documents\gate2023.pdf"
extracted_text = extract_text_from_pdf(file_path)
print(extracted_text[:500])  # Print the first 500 characters of the extracted text