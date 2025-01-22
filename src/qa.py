import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser

def create_llm_chain(context, re_query, model_repo_id="mistralai/Mistral-7B-Instruct-v0.3"):

    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

    hf_model = HuggingFaceEndpoint(
        repo_id=model_repo_id,
        task="text2text-generation"
        )


    prompt_template = """
    You are an AI assistant trained to answer questions about HR policies in a friendly and personalized tone.
    Your responses should:
    1. Be concise and use conversational language.
    2. Address the user directly (e.g., "You are entitled to..." instead of "Employees are entitled to...").
    3. Use only the provided context to answer the query.
    4. If the context does not include the information, respond with: "I'm sorry, but I couldn't find that information in the provided context."

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
