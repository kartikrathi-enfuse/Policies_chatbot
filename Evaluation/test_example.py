import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from embedding import load_faiss_index, load_metadata
from retrieval import retrieve_relevant_chunks
from qa import create_llm_chain

# Load FAISS index and metadata
faiss_index_path = r'D:\RAG\embeddings\hr_policy_faiss.index'
metadata_path = r'D:\RAG\embeddings\hr_policy_faiss_metadata.pkl'

faiss_index = load_faiss_index(faiss_index_path)
metadata = load_metadata(metadata_path)

# Debug: Check FAISS Index Size
print(f"FAISS Index Size: {faiss_index.ntotal}")

# Load the Excel file containing the queries
excel_path = r'C:\Users\kartik.rathi_enfuse-\Desktop\test_sheet_2.xlsx'
df = pd.read_excel(excel_path)

# Process each query in the 'Ques' column
for idx, row in df.iterrows():
    query = row['Ques']

    if pd.isna(query) or query.strip() == "":
        print(f"Skipping empty query at row {idx}")
        df.at[idx, 'Context_extract'] = "N/A"
        df.at[idx, 'Generated_answer'] = "N/A"
        continue  # Skip empty queries

    # Step 1: Retrieve relevant chunks
    retrieved_chunks = retrieve_relevant_chunks(query, index=faiss_index, metadata=metadata, top_k=5)

    if not retrieved_chunks:
        print(f"Warning: No retrieved chunks for query: {query}")
        df.at[idx, 'Context_extract'] = "No relevant context found"
        df.at[idx, 'Generated_answer'] = "No answer generated"
        continue  # Skip to next query

    # Debug: Check retrieved chunks
    # print(f"Retrieved {len(retrieved_chunks)} chunks for query: {query}")

    # Extract context
    context_extract = "\n".join([chunk for chunk, _ in retrieved_chunks])
    df.at[idx, 'Context_extract'] = context_extract

    # Step 2: Generate the answer
    answer = create_llm_chain(context_extract, query)
    df.at[idx, 'Generated_answer'] = answer

# Save the updated DataFrame
output_excel_path = r'D:\RAG\queries_with_answers_3.xlsx'
df.to_excel(output_excel_path, index=False)

print(f"Processing completed. Results saved to '{output_excel_path}'.")
