import os
import chainlit as cl
from main import main  #original code is in `main.py`

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="Understanding Leaves Policies",
            message="Can you explain the company Leaves policies",
            icon="/public/new_img.png",
        ),

        cl.Starter(
            label="Total No. of leaves",
            message="What are the total number of leaves available to the full time employee",
            icon="/public/new_img.png",
        ),
        
        cl.Starter(
            label="Attendence Check-in / Check-out",
            message="What is the correct process for checking in and checking out on Zoho?",
           icon="/public/new_img.png",
        ),
        cl.Starter(
            label="Public Holiday Leaves calendar",
            message="Public Holiday Leaves calendar",
            icon="/public/new_img.png",
        ),
        cl.Starter(
            label="Maternity leave ",
            message="Tell me the details about the maternity leaves. Explain in short",
            icon="/public/new_img.png",
        ),
        cl.Starter(
            label="Where we can report for Sexual harrasement",
            message="Where we can report for Sexual harrasement",
            icon="/public/new_img.png",
        ),
        cl.Starter(
            label="Attendence Regularisation",
            message="How to apply for regularisation of attendence",
            icon="/public/new_img.png",
        )
        
    ]

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
