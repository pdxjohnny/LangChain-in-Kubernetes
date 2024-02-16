# This 
from langchain.prompts import PromptTemplate 
from transformers import pipeline,LlamaForCausalLM,LlamaTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline


custom_prompt_template = """Use the following pieces of information to answer the user's question. Explaining the answer
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Question: {question}

Only return the helpful answer below and nothing else. Give an answer in 1000 characteres at maximum please
Helpful answer:
"""

#prompt = PromptTemplate(template=custom_prompt_template,
#                            input_variables=['question'])
## Load model on HF
efs="/efs_mounted/Models/llama-2-7b-chat-hf"
model_dir = efs
model = LlamaForCausalLM.from_pretrained(model_dir)
tokenizer = LlamaTokenizer.from_pretrained(model_dir)

pipe= pipeline(task="text-generation", model=model, tokenizer=tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01})
        
llm_pipeline = HuggingFacePipeline(pipeline=pipe)