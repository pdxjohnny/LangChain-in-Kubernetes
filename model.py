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
from fastapi import FastAPI, HTTPException, Request
######################
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

class Data(BaseModel):
    field: str

app = FastAPI()
# Allow requests from your React application's origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add the origin of your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your POST endpoint
@app.post("/ws")
async def process_text_data(request: Request):
    try:
        # Get the raw bytes from the request body
        raw_data = await request.body()
        
        # Decode the raw bytes into a string
        text_data = raw_data.decode("utf-8")

        print("Received Data:", text_data)  # Add this line for logging

        answer_from_model = final_result(text_data)

        print(answer_from_model)  # Add this line for logging

        return (answer_from_model['result'])
    except Exception as e:
        print("Error:", str(e))  # Add this line for logging
        raise HTTPException(status_code=500, detail=str(e))

#########################
# Parse the command-line arguments
#parser = argparse.ArgumentParser(description='parser')
#parser.add_argument('--vector_folder', help='folder')
#args = parser.parse_args()

#DB_FAISS_PATH = args.vector_folder
#DB_FAISS_PATH = '/usr/app/src/vectorstore/db_faiss'
DB_FAISS_PATH = '/Users/emlanza/Library/CloudStorage/OneDrive-IntelCorporation/Technical/S2E/Events/Kubecon EU 2024/LangChain-in-Kubernetes/vectorstore/db_faiss'


#DB_FAISS_PATH = "/home/ec2-user/LangChain-in-Kubernetes/vectorstore/db_faiss"


#Define the custom prompt for 
custom_prompt_template = """Use the following pieces of information to answer the user's question. Explaining the answer
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
class chain():
    def __init__(self,DB_FAISS_PATH):
        self.llm_pipeline = None
        self.qa = None
        self.qa_prompt = None
        self.promp = None
        self.faiss_db =None
        
        self.load_model()
        self.qa_bot(DB_FAISS_PATH)
        self.retrieval_qa_chain()

    def load_model(self):

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
        self.llm_pipeline = pipeline(task="text-generation", model=model, tokenizer=tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01, "torch_dtype":torch.bfloat16})

    def retrieval_qa_chain(self):
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm_pipeline,
                                       chain_type='stuff',
                                       retriever=self.faiss_db.as_retriever(search_kwargs={'k': 3}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': self.prompt}
                                       )
    
    def qa_bot(self,DB_FAISS_PATH ):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
        
        self.faiss_db  = FAISS.load_local(DB_FAISS_PATH, embeddings)
    
        self.qa_prompt = set_custom_prompt()
    
    def inference(self,text_input):
        qa = retrieval_qa_chain(self.llm_pipeline, self.qa_prompt, db)
        response = qa({'query': text_input})
        
        return response

test = chain(DB_FAISS_PATH)
result = test.inference("Tell me about kubernetes")
print(result)

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
    print("chain retrieved")
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
    pipeline_path= "/home/ec2-user/LangChain-in-Kubernetes/Data/Pipeline"

    try:
        if os.path.exists(pipeline_path):
            model = AutoModelForCausalLM.from_pretrained(
                pipeline_path,
                    trust_remote_code=True,
                )
            model.eval()

            tokenizer = AutoTokenizer.from_pretrained(pipeline_path)
            pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01, "torch_dtype":torch.bfloat16})
        else:
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
            pipe.save_pretrained(pipeline_path)

    # LangChain HuggingFacePipeline set to our transformer pipeline
    except:
        pass
    llm_local_pipeline = HuggingFacePipeline(pipeline=pipe)

    return llm_local_pipeline


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
    
    local_model_path = "/home/ec2-user/LangChain-in-Kubernetes/Data/embeddings"
    
    if os.path.exists(local_model_path):
        embeddings = HuggingFaceEmbeddings(model_name=local_model_path,model_kwargs={'device': 'cpu'})

    else:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
        
        #embeddings.save_pretrained(local_model_path)
    
    print("here")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    
    print("db loaded")
    
    llm = local_llm()
    print("llm loaded")
    
    qa_prompt = set_custom_prompt()
    
    #qa = retrieval_qa_chain(llm, qa_prompt, db)

    return llm, qa_prompt, db

#output function
def final_result(query):
    #qa_result = qa_bot()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    response = qa({'query': query})
    return response

if __name__ == "__main__":
    test = chain()
    result = test.inference("Tell me about kubernetes")
    print(result)
    #Initiate model class to have chain loaded in memory 
    #llm, qa_prompt, db = qa_bot()
    #uvicorn.run(app, host="localhost", port=8000)
    

####################################################
""" #chainlit code
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

    await cl.Message(content=answer).send() """