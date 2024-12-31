from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from a given PDF."""
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_pdfs(pdf_folder):
    """Extract text from all PDFs in the folder."""
    all_text = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing file: {filename}")
            pdf_text = extract_text_from_pdf(pdf_path)
            all_text.append(pdf_text)
    return all_text

if __name__ == "__main__":
    print(extract_text_from_pdfs('D:\RAG\Data')[0])
