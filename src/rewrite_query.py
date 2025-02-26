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
    model = genai.GenerativeModel(model_name='gemini-2.0-flash', generation_config=generation_config)

    # Define the prompt
    prompt = f"""
    Correct any grammatical errors in the following query while preserving its original meaning.
    Only fix spelling, punctuation, or sentence structure issues.
    If no correction is needed, return the query exactly as it is, without additional explanation.

    Query: {query}
    """

    # Generate response
    response_jd = model.generate_content([prompt])

    # Extract and return the text
    return response_jd.parts[0].text

# Example usage
if __name__ == "__main__":
    query = "What is the attendance and punctuality polici?"
    rewritten_query = rewrite_query_for_rag(query)
    print(rewritten_query)
