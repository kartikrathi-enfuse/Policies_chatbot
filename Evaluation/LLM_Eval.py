import google.generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd
import re  # Regular expression module for more robust parsing
import time  # For adding delay between API calls
import random  # For randomizing wait times

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

def gemini_evaluation(query, answer, context):
    """
    Use Gemini to evaluate the Faithfulness, Context Precision, and Answer Relevancy metrics.
    """
    prompt = f"""
    Evaluate the following in terms of Faithfulness, Context Precision, and Answer Relevancy:
    Faithfulness: Does the answer accurately reflect the context provided?
    Context Precision: How well does the answer relate to the context extract?
    Answer Relevancy: How relevant is the answer to the query?

    Query: {query}
    Context: {context}
    Answer: {answer}

    Provide the scores for each metric on a scale of 0 to 1:
    - Faithfulness
    - Context Precision
    - Answer Relevancy
    """

    # Generate the response from Gemini
    response = model.generate_content([prompt])

    # Extract the result
    result_text = response.parts[0].text.strip()

    # Use regular expressions to capture scores for Faithfulness, Context Precision, and Answer Relevancy
    try:
        faithfulness_match = re.search(r'Faithfulness:\s*(\d+\.?\d*)', result_text)
        context_precision_match = re.search(r'Context Precision:\s*(\d+\.?\d*)', result_text)
        answer_relevancy_match = re.search(r'Answer Relevancy:\s*(\d+\.?\d*)', result_text)

        # Extract the scores from the regex matches
        faithfulness = float(faithfulness_match.group(1)) if faithfulness_match else None
        context_precision = float(context_precision_match.group(1)) if context_precision_match else None
        answer_relevancy = float(answer_relevancy_match.group(1)) if answer_relevancy_match else None

        return faithfulness, context_precision, answer_relevancy
    except Exception as e:
        print(f"Error parsing result: {e}")
        return None, None, None

def process_and_evaluate(file_path, output_file):
    # Load the data
    df = pd.read_excel(file_path)

    # Initialize result lists
    faithfulness_scores = []
    context_precision_scores = []
    answer_relevancy_scores = []

    # Process each row and calculate the scores
    for index, row in df.iterrows():
        question = row['Ques']
        answer = row['Generated_answer']
        context = row['Context_extract']

        # Retry mechanism to handle resource exhaustion
        retries = 3
        success = False
        for attempt in range(retries):
            try:
                # Call Gemini to get the error metrics
                faithfulness, context_precision, answer_relevancy = gemini_evaluation(question, answer, context)
                # Append the results to the lists
                faithfulness_scores.append(faithfulness)
                context_precision_scores.append(context_precision)
                answer_relevancy_scores.append(answer_relevancy)
                success = True
                break  # If successful, break out of the retry loop
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    wait_time = random.uniform(2, 5)  # Randomized wait time between 2-5 seconds
                    print(f"Retrying after {wait_time:.2f} seconds...")
                    time.sleep(wait_time)
                else:
                    print("All retry attempts failed. Skipping this entry.")

        if not success:
            # If all retries fail, append None for the scores
            faithfulness_scores.append(None)
            context_precision_scores.append(None)
            answer_relevancy_scores.append(None)

        # Optional: Add a delay between each request to avoid overwhelming the system
        time.sleep(random.uniform(3, 5))  # Random delay between 1-2 seconds

    # Add the scores to the DataFrame
    df['Faithfulness'] = faithfulness_scores
    df['Context Precision'] = context_precision_scores
    df['Answer Relevancy'] = answer_relevancy_scores

    # Save the results to a new Excel file
    df.to_excel(output_file, index=False)

# File paths
input_file = "D:\RAG\queries_with_answers_3.xlsx"  # Update with the path to your input Excel file
output_file = "output_with_metrics_1.xlsx"  # Path where the output will be saved

# Run the process
process_and_evaluate(input_file, output_file)

print("Process completed and metrics have been saved to the output file.")
