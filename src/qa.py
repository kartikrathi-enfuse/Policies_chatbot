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
    You are an AI assistant trained to answer questions about HR policies in structured format.
    Given the following context and user query, provide a concise and accurate answer.Dont include any Note, Steps and Extra information.

    Context:
    {context}

    Query:
    {query}

    Answer:
    """

    prompt = PromptTemplate(
        input_variables=["context", "re_query"],
        template=prompt_template
    )

    chain = prompt | hf_model | StrOutputParser()

    return chain.invoke({'context': context, 'query': re_query})



# def create_llm_chain(model_repo_id="mistralai/Mistral-7B-Instruct-v0.3"):
#     """Create the LangChain LLM chain for question answering."""
#     os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
#     hf_model = HuggingFaceEndpoint(
#         repo_id=model_repo_id,
#         task="text2text-generation"
#     )

#     prompt_template = """
#     You are an AI assistant trained to answer questions about HR policies in structured format.
#     Given the following context and user query, provide a concise and accurate answer.Dont include headlines.
    
#     Context:
#     {context}

#     Query:
#     {query}

#     Answer:
#     """

#     prompt = PromptTemplate(
#         input_variables=["context", "re_query"],
#         template=prompt_template
#     )

#     return LLMChain(llm=hf_model, prompt=prompt)

# def get_answer(llm_chain, context, re_query):
#     # Create a refined prompt that combines context and query
#     # prompt = f"Context: {context}\n\nQuery: {re_query}\n\nAnswer:"

#     # Invoke the LLM chain with the combined prompt
#     return llm_chain.invoke({'context': context, 'query': re_query})
