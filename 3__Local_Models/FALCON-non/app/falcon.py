from transformers import AutoTokenizer, AutoModelForCausalLM,pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

model_path="/efs_mounted/Models/Falcon-7b-instruct"
local_model = AutoModelForCausalLM.from_pretrained(model_path, return_dict=True)
local_tokenizer = AutoTokenizer.from_pretrained(model_path)
local_model.eval()

pipe= pipeline(task="text-generation", model=local_model, tokenizer=local_tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01})  

#Pipeline to be consumed by Langserve API
llm_pipeline = HuggingFacePipeline(pipeline=pipe)