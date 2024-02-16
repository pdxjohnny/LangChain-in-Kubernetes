from fastapi import FastAPI, Request, Request,HTTPException
from langserve import RemoteRunnable
from langchain.prompts.chat import ChatPromptTemplate
from fastapi.responses import PlainTextResponse
from fastapi import Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi import Header
import os 
import pathlib
from pprint import pprint

import yaml
import kubernetes
import kubernetes.client
from kubernetes.client.rest import ApiException
from kubernetes import client, config

def kubernetes_ipv4_address_for_pod_name(pod_name):
    # Load the service account kubeconfig
    configuration = kubernetes.client.Configuration()
    config.load_incluster_config(client_configuration=configuration)

    namespace = pathlib.Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace").read_text()

    with kubernetes.client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = kubernetes.client.DiscoveryV1Api(api_client)

        api_response = api_instance.list_namespaced_endpoint_slice(namespace)

    found_endpoint = None
    for endpoint_slice in api_response.items:
        for endpoint in endpoint_slice.endpoints:
            if pod_name.strip() in endpoint.target_ref.name:
                found_endpoint = endpoint
                break
        if found_endpoint:
            break
    if not found_endpoint:
        raise Exception(f"Pod {pod_name} not found")

    # TODO Handle more cases than zeroith index?
    return found_endpoint.addresses[0]

pod_openai_api= kubernetes_ipv4_address_for_pod_name("chatopenai")
print(kubernetes_ipv4_address_for_pod_name("chatopenai"))

class Data(BaseModel):
    question: str

app = FastAPI()

# Allow all origins with necessary methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  # Add comma here
    allow_headers=["*"],  # Add comma here
    allow_credentials=False,
)
openai_llm = RemoteRunnable("http://10.100.59.107:80/openai_api").with_types(input_type=str)
llama_chain = RemoteRunnable("http://10.100.53.180:80/llama_chain").with_types(input_type=str)
falcon_non_chain = RemoteRunnable("http://10.100.236.142:80/falcon_chain").with_types(input_type=str)

@app.post("/api_local_llama", response_class=PlainTextResponse)
async def process_text_data(question: Data,user_agent: str = Header(None)):

    try:
        user_question= str(question.question)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a highly educated person who loves to use big words. "
                    + "You are also concise. Never answer in more than three sentences.",
                ),
                ("human", user_question),
            ]       
        ).format_messages()     
        result = llama_chain.invoke(prompt)  # Pass the extracted question
        print(result.content)
        
        return result.content
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    
 
@app.post("/apiopenai")
async def process_text_data(question: Data,user_agent: str = Header(None)):
    try:
        user_question= str(question.question)
        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a highly educated person who loves to use big words. "
                    + "You are also concise. Never answer in more than three sentences.",
                ),
                ("human", user_question),
            ]       
        ).format_messages()     
        
                # Pass the extracted question
        result=openai_llm.invoke(prompt)
        
        return result.content
    
    except Exception as e:
        print("Entering ERROR block...")
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    
@app.post("/api_local_falcon_non")
async def process_text_data(question: Data,user_agent: str = Header(None)):
    try:
        user_question= str(question.question)

        result=falcon_non_chain.invoke({"question": user_question})
        
        return result
    
    except Exception as e:
        print("Entering ERROR block...")
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


if __name__=='__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)