from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline
from getpass import getpass
from langchain.chains import RetrievalQA
from transformers import pipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

#DB_FAISS_PATH = '/usr/app/src/chat/vectorstore/db_faiss'

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
        self.prompt = None
        self.faiss_db =None
        self.custom_prompt_template = """Use the following pieces of information to answer the user's question. Explaining the answer
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context: {context}
            Question: {question}

            Only return the helpful answer below and nothing else.
            Helpful answer:
            """
        print("Starting the model")
        self.load_model()
        print("Starting bot")
        self.qa_bot(DB_FAISS_PATH)
        print("Starting the chain")
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
        pipe= pipeline(task="text-generation", model=model, tokenizer=tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01, "torch_dtype":torch.bfloat16})
        
        self.llm_pipeline = HuggingFacePipeline(pipeline=pipe)

    def retrieval_qa_chain(self):
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm_pipeline,
                                       chain_type='stuff',
                                       retriever=self.faiss_db.as_retriever(search_kwargs={'k': 3}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': self.qa_prompt}
                                       )
    
    def qa_bot(self,DB_FAISS_PATH ):
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
        
        self.faiss_db  = FAISS.load_local(DB_FAISS_PATH, embeddings)
        
        prompt = PromptTemplate(template=self.custom_prompt_template,
                            input_variables=['context', 'question'])
        

        
        self.qa_prompt = prompt
    
    def inference(self,text_input):
        qa = self.retrieval_qa_chain(self.llm_pipeline, self.qa_prompt, self.faiss_db)
        response = qa({'query': text_input})
        
        return response
