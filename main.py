import os
import faiss
import pickle
from src.chunking import chunk_text_from_all_pdfs
from src.pdf_extraction import extract_text_from_pdfs
from src.embedding import generate_embeddings
from src.retrieval import retrieve_relevant_chunks
from src.embedding import is_faiss_index_empty, create_faiss_index, save_faiss_index, load_faiss_index, load_metadata
from src.qa import create_llm_chain  # Assuming these are in a separate file
from src.rewrite_query import rewrite_query_for_rag
from src.router import is_general_question
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

def main(pdf_folder, query):
    # Define FAISS index and metadata paths
    faiss_index_path = "embeddings/hr_policy_faiss.index"
    metadata_path = "embeddings/hr_policy_faiss_metadata.pkl"

    # Check if FAISS index is empty or doesn't exist
    if is_faiss_index_empty(faiss_index_path):
        print("FAISS index is empty or does not exist. Processing PDFs...")

        # Step 1: Extract text from PDFs
        pdf_texts = extract_text_from_pdfs(pdf_folder)

        # Step 2: Chunk the extracted text
        all_chunks = chunk_text_from_all_pdfs(pdf_texts)

        # Step 3: Generate embeddings for all chunks
        embeddings = generate_embeddings(all_chunks)

        # Step 4: Create and store FAISS index
        index = create_faiss_index(embeddings)
        save_faiss_index(index, faiss_index_path, all_chunks, metadata_path)

        print(f"FAISS index saved at {faiss_index_path}")
        print(f"Metadata saved at {metadata_path}")
    else:
        print("FAISS index already exists. Skipping chunking and embedding.")

    #Load FAISS index and metadata
    index = load_faiss_index(faiss_index_path)
    metadata = load_metadata(metadata_path)

    #handling greeting msg
    if is_general_question(query):
        return "Hello! How can I assist you"

    #Rewrite the Query
    re_query = rewrite_query_for_rag(query)
    print(re_query)

    # Step 6: Retrieve relevant chunks based on the query
    retrieved_chunks = retrieve_relevant_chunks(re_query, index, metadata, top_k=8)

    if not retrieved_chunks:
        return "Sorry, I dont have answer for your question. Please mail your query ==> hr@enfuse-solutions.com"

    else:
        # Step 7: Get the answer using the retrieved context
        # llm_chain = create_llm_chain()
        context = "\n".join([chunk for chunk, _ in retrieved_chunks])
        output = create_llm_chain(context=context, re_query=re_query)

    # print(f"Answer: {answer}")
    # print("--------------------------------")
    # print(output)
    return output


if __name__ == "__main__":
    pdf_folder = r"D:\RAG\Data"
    query = "What is the procedure to take 5 or more days leave"
    print(main(pdf_folder, query))