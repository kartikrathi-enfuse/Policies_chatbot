from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_into_chunks(text, chunk_size=512, chunk_overlap=55):
    """Split text into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)

def chunk_text_from_all_pdfs(pdf_texts, chunk_size=512, chunk_overlap=55):
    """Chunk text from all PDF files."""
    all_chunks = []
    for pdf_text in pdf_texts:
        chunks = split_text_into_chunks(pdf_text, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
    return all_chunks
