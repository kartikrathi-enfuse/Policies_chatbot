from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

def is_faiss_index_empty(faiss_index_path):
    """Check if the FAISS index is empty or does not exist."""
    if not os.path.exists(faiss_index_path):
        return True
    # Optionally check if the FAISS index has no vectors
    import faiss
    index = faiss.read_index(faiss_index_path)
    if index.ntotal == 0:
        return True
    return False

def generate_embeddings(chunks, model_name='sentence-transformers/paraphrase-MiniLM-L6-v2'):
    """Generate embeddings for the given chunks using the SentenceTransformer."""
    embedding_model = SentenceTransformer(model_name)
    embeddings =  embedding_model.encode(chunks, show_progress_bar=True).astype(np.float32)
    faiss.normalize_L2(embeddings) #Use norm for cosine similarity
    return embeddings

def create_faiss_index(embeddings):
    """Create a FAISS index for cosine sim and add embeddings."""
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index

def save_faiss_index(index, faiss_index_path, metadata, metadata_path):
    """Save the FAISS index and metadata."""
    faiss.write_index(index, faiss_index_path)
    with open(metadata_path, 'wb') as metadata_file:
        pickle.dump(metadata, metadata_file)

def load_faiss_index(faiss_index_path):
    """Load the FAISS index."""
    return faiss.read_index(faiss_index_path)

def load_metadata(metadata_path):
    """Load metadata for the FAISS index."""
    with open(metadata_path, 'rb') as metadata_file:
        return pickle.load(metadata_file)
