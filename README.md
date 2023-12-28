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
Create Python Back End container
```{python}
    cd chat-backend
    docker build --platform linux/amd64 -t chat:latest .
```
You should now be able to see both containers on your environment.
```{python}
    docker images
```
# 2. Make all containers run FRONT_END and BACK_END.

```{python}
    docker run -p 3000:3000 front_end:latest

    docker run -p 8000:8000 front_end:latest
```
This command will start both containers at each port. Front end will be using port 3000 and the back_end service will run on port 8000.

You should now be able to see the chatbot interface on http://localhost:3000


# Optimization step
The front end can interact with both optimized and non-optimzed models. You can find in the folder chat-backend Optimized the model already optimized.

This is the step by step if you want to know how we did it: 

    1. Clone Intel neural compressor 
    ```{python}
    git clone https://github.com/intel/neural-compressor.git
    ```

    2. Go to the folder to perform the quantization
    ```{python}
    cd neural-compressor/examples/pytorch/nlp/huggingface_models/language-modeling/quantization/llm
    ```

    

# OPTIONAL If you have AWS ECR

# Deploy it on Kubernetes



