import pandas as pd
from src.embedding import load_faiss_index, load_metadata
from src.retrieval import retrieve_relevant_chunks
from src.qa import create_llm_chain
from src.rewrite_query import rewrite_query_for_rag  

# Load FAISS index and metadata
faiss_index_path = r'D:\RAG\embeddings\hr_policy_faiss.index'
metadata_path = r'D:\RAG\embeddings\hr_policy_faiss_metadata.pkl'

# Load the FAISS index and metadata
faiss_index = load_faiss_index(faiss_index_path)
metadata = load_metadata(metadata_path)

# Load the Excel file containing the queries
excel_path = r'C:\Users\kartik.rathi_enfuse-\Desktop\test_sheet_2.xlsx'
df = pd.read_excel(excel_path)

# Process each query in the 'Ques' column
for idx, row in df.iterrows():
    query = row['Ques']

    # Step 1: Rewrite the query using the rewrite_query_for_rag function
    rewritten_query = rewrite_query_for_rag(query)
    df.at[idx, 'Rewritten_Query'] = rewritten_query  # Store the rewritten query in the DataFrame

    # Step 2: Retrieve relevant chunks using the rewritten query
    retrieved_chunks = retrieve_relevant_chunks(rewritten_query, index=faiss_index, metadata=metadata, top_k=3)
    context_extract = "\n".join([chunk for chunk, _ in retrieved_chunks])
    df.at[idx, 'Context_extract'] = context_extract  # Store the retrieved context in the DataFrame

    # Step 3: Generate the answer using the context and rewritten query
    answer = create_llm_chain(context_extract, rewritten_query)
    # generated_answer = answer['text']
    df.at[idx, 'Generated_answer'] = answer  # Store the generated answer in the DataFrame

# Save the updated DataFrame to the Excel file
output_excel_path = r'D:\RAG\queries_with_answers_3.xlsx'
df.to_excel(output_excel_path, index=False)

print(f"Processing completed. Results saved to '{output_excel_path}'.")
