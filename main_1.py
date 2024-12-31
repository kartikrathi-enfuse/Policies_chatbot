import os
import chainlit as cl
from main import main  #original code is in `main.py`

# Chainlit handler for chatbot startup
@cl.on_chat_start
async def on_startup():
    """
    Send a welcome message when the chatbot starts.
    """
    welcome_message = "Hey, I'm your HR policy chatbot. Please ask a question!"
    await cl.Message(
        content=welcome_message,
    ).send()

# Wrapper to interact with the main function
@cl.on_message
async def process_query(message: cl.Message):
    """
    Chainlit handler to process user queries via the frontend.
    """
    pdf_folder = "Data/"  # Folder containing PDFs
    query = message.content  # Get the query from the Chainlit frontend

    # Redirecting the main logic to process the query
    try:
        # Call the main function with query and folder
        print(f"Processing query: {query}")
        result = main(pdf_folder, query)
        
        if isinstance(result, str):
            result_list = result.split("\n")
        elif isinstance(result, list):
            result_list = result
        else:
            result_list = [str(result)]

        formatted_result = "\n".join([f"{point.strip()}" for point in result_list if point.strip()])        

        # Display the result in the frontend 
        await cl.Message(content=formatted_result).send()
    except Exception as e:
        # Display error messages in the frontend 
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        await cl.Message(content=error_message).send()
