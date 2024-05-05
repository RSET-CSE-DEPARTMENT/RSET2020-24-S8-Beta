import PyPDF2

def read_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# pdf_path = 'marketing.pdf'
# text = read_pdf(pdf_path)
# print(text,end=" ")