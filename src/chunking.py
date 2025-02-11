from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def split_text_into_chunks(text, chunk_size=650, chunk_overlap=70):
    """Split text into smaller chunks without breaking sentences."""
    # Regular expression to match sentence boundaries (., ?, !, etc.)
    sentence_endings = re.compile(r'([.!?])\s+')

    # Split the text into sentences based on sentence-ending punctuation
    sentences = sentence_endings.split(text)

    # Reconstruct the sentences correctly
    sentences = [sentences[i] + sentences[i+1] for i in range(0, len(sentences)-1, 2)]

    # Add the last sentence if the text ended without punctuation at the end
    if len(sentences) * 2 != len(sentence_endings.findall(text)):
        sentences.append(sentences[-1] + sentences[-2])

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Check if adding this sentence will exceed chunk_size
        if len(current_chunk) + len(sentence) + 1 > chunk_size:
            # If it exceeds, save the current chunk and start a new one
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            # Otherwise, append the sentence to the current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

    # Add any remaining content as the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def chunk_text_from_all_pdfs(pdf_texts, chunk_size=650, chunk_overlap=70):
    """Chunk text from all PDF files."""
    all_chunks = []
    for pdf_text in pdf_texts:
        chunks = split_text_into_chunks(pdf_text, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
    return all_chunks