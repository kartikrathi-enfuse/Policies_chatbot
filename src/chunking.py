from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(text, chunk_size=1200, chunk_overlap=150):
    """Split text into smaller chunks while preserving sentence boundaries using RecursiveCharacterTextSplitter."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[". ", "? ", "! ", "\n"]  # Ensuring sentences are not split midway
    )

    return text_splitter.split_text(text)

def chunk_text_from_all_pdfs(pdf_texts, chunk_size=650, chunk_overlap=70):
    """Chunk text from all PDF files using RecursiveCharacterTextSplitter."""
    all_chunks = []
    for pdf_text in pdf_texts:
        chunks = split_text_into_chunks(pdf_text, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
    return all_chunks
