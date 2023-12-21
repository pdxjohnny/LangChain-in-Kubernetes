# DEMO for deploying in K8S a RAG chatbot WITHOUT using external paid APIs.

This repository is intented to share a Kubernetes implementation for a RAG chatbot using Open source tools:
1. The LLM model will be downloaded to a POD to avoid the usage of external paid APIs. We selected Falcon 7B Instruct model In this case the repo provides 2 options : Optimized LLM and not-optimized LLM
2. The vector database used is FAISS. 
3. It was built using LangChain 
4. The front end is a REACT application

This is a reference implementation of a question answering for a RAG implementation using Langchain

In these demos, you will explore how RAG ( Retrieval-Augmented Generation ) can enhance AI models by leveraging external data sources to provide context-aware answers and unlock insights.

# 1. Create FRONT_END and BACK_END containers

Go to each Folder to create each container (docker). There is a dockerfile on each folder with the instructions (In this case we will add it as an Intel processor) :

Create REACT front end container
```{python}
    cd front_end
    docker build --platform linux/amd64 -t front_end:latest .
```
Create Python Back end container
```{python}
    cd chat-backend
    docker build --platform linux/amd64 -t chat:latest .
```
# OPTIONAL If you have AWS ECR

# Deploy it on Kubernetes



