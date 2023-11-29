from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.llms import HuggingFaceHub
from langchain.llms import HuggingFacePipeline
from getpass import getpass
from langchain.chains import RetrievalQA
import chainlit as cl
import os
import argparse
from transformers import pipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='parser')
parser.add_argument('--vector_folder', help='folder')
args = parser.parse_args()

DB_FAISS_PATH = args.vector_folder
#DB_FAISS_PATH = 'vectorstore/db_faiss'

#Define the custom prompt for 
custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

#Retrieval QA Chain
#https://js.langchain.com/docs/modules/chains/popular/vector_db_qa
def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 3}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return qa_chain

#Loading the models
#Using Hugging face hub
def load_llm():
    HUGGINGFACEHUB_API_TOKEN = "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"

    #HUGGINGFACEHUB_API_TOKEN = getpass()
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

    repo_id = "databricks/dolly-v2-3b"

    llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64})

    return llm

def local_llm():
    #Set model
    model = "tiiuae/falcon-7b-instruct"
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model)
    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        model,
        trust_remote_code=True,
        )
    # Set to eval mode
    model.eval()
    # Create a pipline
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01, "torch_dtype":torch.bfloat16})
    # LangChain HuggingFacePipeline set to our transformer pipeline
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm


# Loading the model locally 

#USING C TRANSFORMER
##def load_llm():
    # Load the locally downloaded model here
#    llm = CTransformers(
#        model = "TheBloke/Llama-2-7B-Chat-GGML",
#        model_type="llama",
#        max_new_tokens = 512,
#        temperature = 0.5
#    )
#    return llm

#QA Model Function
def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    
    llm = local_llm()
    
    qa_prompt = set_custom_prompt()
    
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa

#output function
def final_result(query):
    qa_result = qa_bot()
    response = qa_result({'query': query})
    return response

####################################################
#chainlit code
@cl.on_chat_start
async def start():
    chain = qa_bot()
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to Medical Bot. What is your query?"
    await msg.update()

    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain") 
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["result"]
    sources = res["source_documents"]

    if sources:
        answer += f"\nSources:" + str(sources)
    else:
        answer += "\nNo sources found"

    await cl.Message(content=answer).send()