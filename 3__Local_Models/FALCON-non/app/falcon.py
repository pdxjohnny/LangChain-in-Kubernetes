# This 
from langchain.prompts import PromptTemplate 
from transformers import AutoTokenizer, AutoModelForCausalLM,pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline


custom_prompt_template = """Use the following pieces of information to answer the user's question. Explaining the answer
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Question: {question}

Only return the helpful answer below and nothing else. Give an answer in 1000 characteres at maximum please
Helpful answer:
"""

model_path="/efs_mounted/Models/Falcon-7b-instruct"
local_model = AutoModelForCausalLM.from_pretrained(model_path, return_dict=True)
local_tokenizer = AutoTokenizer.from_pretrained(model_path)
local_model.eval()

pipe= pipeline(task="text-generation", model=local_model, tokenizer=local_tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01})  

llm_pipeline = HuggingFacePipeline(pipeline=pipe)

template = """Use the following pieces of information to answer the user's question. Explaining the answer
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Question: {question}

Only return the helpful answer below and nothing else. Give an answer in 1000 characteres at maximum please
Helpful answer:
"""

prompt = PromptTemplate.from_template(template)   

chain = prompt | llm_pipeline