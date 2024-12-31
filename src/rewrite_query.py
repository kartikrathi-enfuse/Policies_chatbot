import google.generativeai as genai
from dotenv import load_dotenv
import os

def rewrite_query_for_rag(query):
    # Load environment variables
    load_dotenv()

    # Configure the Generative AI API
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Define the generation configuration
    generation_config = {
        'temperature': 0,
        'max_output_tokens': 8000,
        'top_p': 0.2
    }

    # Initialize the model
    model = genai.GenerativeModel(model_name='gemini-pro', generation_config=generation_config)

    # Define the prompt
    prompt_jd = f"""
    Rewrite the given user query to make it precise and specific for retrieving accurate information from a
    retrieval-augmented generation (RAG) system. Focus on HR policies and include all relevant details to ensure clarity.
    Dont include any additional information to the input query. ** USER BELONGS TO INDIA **

    Args:
        user_query (str): Original query {query} from the user.

    Returns:
        str: Rewritten query for accurate retrieval.
    """

    # Generate response
    response_jd = model.generate_content([prompt_jd])

    # Extract and return the text
    return response_jd.parts[0].text

# Example usage
if __name__ == "__main__":
    query = "What is the procedure to take 5 or more days leave"
    rewritten_query = rewrite_query_for_rag(query)
    print(rewritten_query)
