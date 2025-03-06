import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

def create_llm_chain(context, re_query, model_repo_id="mistralai/Mistral-7B-Instruct-v0.3"):
    api_key = os.getenv("GOOGLE_API_KEY")

    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=api_key,temperature=0.5)

    prompt_template = """
    You are an AI assistant trained to answer Enfuse Solutions Employees questions about HR policies in a friendly and personalized tone.
    **IMPORTANT RULES **
    - You **MUST** only use the provided context to answer the query.
    - If the answer is **not explicitly mentioned in the context **, say :
    ** I'm sorry, but I don't have that information.Please mail your query to hr@enfusesolutions.com for assistance.**
    - **Don't infer, assume, or generate new information **
    - Be concise, direct and Conversational.
    - Address the user directly (e.g., "You are entitled to..." instead of "Employees are entitled to...").
    - You must give answer from the provided context only.

    Context:
    {context}

    Query:
    {query}

    Personalized Answer:
    """

    prompt = PromptTemplate(
        input_variables=["context", "re_query"],
        template=prompt_template
    )

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({'context': context, 'query': re_query})


if __name__ == '__main__':
    context = '''If an employee calls out of work the day before, the day of, or the day after a holiday, the 
    manager will review the circumstances of the absence. Based on this review, the manager 
    has the discretion to determine whether to count the incident as a regular occurrence or go
    start day   
    ▪ 5 or more leaves: A leave request must be submitted at least 10 days before the leave 
    start day
    6 Instances    Step 3: Final written warning/show cause    
    Beyond 6 Instances    Step 4: Termination    
    3 days    Step 1: Verbal warning    
    Total # of Days Absent    5 days    Step 2: Written warning & absconding 
    trigger    
    Consecutive or Non - '''

    re_query = "How many days prior should I inform to manager if i want 7 days leave?"
    print(create_llm_chain(context,re_query))