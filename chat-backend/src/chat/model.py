from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline
from getpass import getpass
from langchain.chains import RetrievalQA
from transformers import pipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM,LlamaForCausalLM,LlamaTokenizer
import torch

#DB_FAISS_PATH = '/usr/app/src/chat/vectorstore/db_faiss'

custom_prompt_template = """Use the following pieces of information to answer the user's question. Explaining the answer
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else. Give an answer in 1000 characteres at maximum please
Helpful answer:
"""
class chain():
    def __init__(self,DB_FAISS_PATH,name_model):
        self.llm_pipeline = None
        self.qa = None
        self.qa_prompt = None
        self.prompt = None
        self.faiss_db =None
        self.name_model = name_model
        self.custom_prompt_template = """Use the following pieces of information to answer the user's question. Explaining the answer
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context: {context}
            Question: {question}

            Only return the helpful answer below and nothing else. Make your answer concise and it wouldn't take more than 1000 characters.
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
        if self.name_model=="Llama":
            # Download the model from Meta site 
            ####### YOU WILL NEED TO FOLLOW THE PROCESS IN ORDER TO DOWNLOAD THE MODEL

            # FOR THIS EXAMPLE I'VE DOWNLOADED THE MODEL ON A MODELS FOLDER AND CONVERT THEM TO A HF FORMAT
            # INSTRUCTIONS IN THE README FILE https://ai.meta.com/blog/5-steps-to-getting-started-with-llama-2/
            # Steps. 1- download with the script, 2- convert 

            model_dir = "/usr/app/src/chat/Models/llama-2-7b-chat-hf"
            
            model = LlamaForCausalLM.from_pretrained(model_dir)
            tokenizer = LlamaTokenizer.from_pretrained(model_dir)

        if self.name_model=="Falcon":
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
        # Bulild the Prompt

        response = self.qa_chain({'query': text_input})
        
        return response
