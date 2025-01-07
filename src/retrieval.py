from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def retrieve_relevant_chunks(query, index, metadata, top_k, model_name='all-MiniLM-L6-v2',threshold=1.5):
    """Retrieve top_k relevant chunks from the FAISS index."""
    embedding_model = SentenceTransformer(model_name)
    query_embedding = embedding_model.encode([query]).astype(np.float32)

    distances, indices = index.search(query_embedding, top_k)
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx != -1 and dist <= threshold:  # Valid index
            results.append((metadata[idx], dist))

    return results


if __name__ == '__main__':
    from embedding import load_faiss_index, load_metadata
    query = 'Is there any plateform on which I have to apply for the leaves ?'
    faiss_index_path = r"D:\RAG\embeddings\hr_policy_faiss.index"
    metadata_path = r"D:\RAG\embeddings\hr_policy_faiss_metadata.pkl"
    index = load_faiss_index(faiss_index_path)
    metadata = load_metadata(metadata_path)
    print(retrieve_relevant_chunks(query, index, metadata, top_k=4, model_name='all-MiniLM-L6-v2'))