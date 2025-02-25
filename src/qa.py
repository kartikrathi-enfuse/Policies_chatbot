import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def create_llm_chain(context, re_query, model_repo_id="mistralai/Mistral-7B-Instruct-v0.3"):
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    hf_model = HuggingFaceEndpoint(
        repo_id=model_repo_id,
        task="text2text-generation",
        temperature=0.2
        )

    prompt_template = """
    You are an AI assistant trained to answer questions about HR policies in a friendly and personalized tone.
    Your responses should:
    1. Be concise, Short and use conversational language.
    2. Address the user directly (e.g., "You are entitled to..." instead of "Employees are entitled to...").
    3. Use only the provided context to answer the query. **Don't assume, infer or generate any new information**.
    4. If the context does not include the information, respond with: "I'm sorry, but I Dont have the information "
    5. Avoid Phrases like "In the provided context " or "Based on Given context " .

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

    chain = prompt | hf_model | StrOutputParser()

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