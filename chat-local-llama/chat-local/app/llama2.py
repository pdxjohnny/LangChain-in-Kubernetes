# This 
from langchain.prompts import PromptTemplate 
from transformers import pipeline,LlamaForCausalLM,LlamaTokenizer
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain


custom_prompt_template = """Use the following pieces of information to answer the user's question. Explaining the answer
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Question: {question}

Only return the helpful answer below and nothing else. Give an answer in 1000 characteres at maximum please
Helpful answer:
"""

prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['question'])
print("MODEL LOADED")
## Load model on HF
model_dir = "/efs_mounted/Models/llama-2-7b-chat-hf"
model = LlamaForCausalLM.from_pretrained(model_dir)
tokenizer = LlamaTokenizer.from_pretrained(model_dir)

pipe= pipeline(task="text-generation", model=model, tokenizer=tokenizer, 
                         trust_remote_code=True, max_new_tokens=100, 
                         repetition_penalty=1.1, model_kwargs={"max_length": 1200, "temperature": 0.01})
        
llm_pipeline = HuggingFacePipeline(pipeline=pipe)

chain = prompt | llm_pipeline

#chain = LLMChain(llm=llm_pipeline, prompt=prompt)

#ESTO ES LO QUE VA A EXPONER LANGSERV
#print("Corriendo la consulta")
#print(chain.run({"question": "Tell me about kubernetes"}))
#chain.run
