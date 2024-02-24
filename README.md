# DEMO for deploying a QA chatbot in K8S

This repository is intented to share a Kubernetes implementation for a chatbot using Open source tools:
This is the architecture intended

Since it's using local models we will rely on AWS File server(EFS) and container registry (ECR) for practical purposes. You can refer to your own File server and your own 

# Description
1. Front_End
The front End is based on react-chatbot-kit  https://www.npmjs.com/package/react-chatbot-kit

2.  Models
The implementation uses 3 models : 
- Local LLaMa2_7B : Downloaded from Meta and stored on a file server (EFS)
- Local Optimized LLaMa2_7B :Model optimized using ITREX (Details on XXX Optimization section), stored on a file server (EFS)
- External paid API : In this example we used OpenAI.

# Architecture

## Description 

# 1. Pods creation

# 2. Kubernetes
## 2.1 Configure cluster
### Install ngnix
### Install Storage drivers
### Install Grafana for visualization
Instalation of grafana POD 
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus

This installed grafana and prometheus

sudo kubectl port-forward service/grafana 1002:80

kubectl exec -it <pod_name> -n default -- bash
The password should be reseted

grafana-cli admin reset-admin-password admin



# Optimization section

We will be using Intel Extension for transformers to optimize LLaMa2 7B model. This step will help to reduce the size of the model from ~30GB to 14GB. Thanks to techiques like quantization.

git clone https://github.com/intel/intel-extension-for-transformers.git
cd  intel-extension-for-transformers
pip install -r requirement.txt
python setup.py install

This is a reference implementation of a question answering for a RAG implementation using Langchain

In these demos, you will explore how RAG ( Retrieval-Augmented Generation ) can enhance AI models by leveraging external data sources to provide context-aware answers and unlock insights.

Note: The embeddings needed to 

# 1. Create front_end and back_end containers (Containers could live in an Intel docker Hub)

After clonning the projetc go to each Folder to create each container (docker). There is a dockerfile on each folder with the instructions (In this case we will add it as an Intel processor) :

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
# 2. TEST IT : Containers test Make all containers run FRONT_END and BACK_END.

```{python}
    docker run -p 3000:3000 front_end:latest

    docker run -p 8000:8000 front_end:latest
```
This command will start both containers at each port. Front end will be using port 3000 and the back_end service will run on port 8000.

You should now be able to see the chatbot interface on http://localhost:3000

# Let's move to the kubernetes part
The solution counts with a yaml file which deploys these 2 containers + ingress

# 3 Optimization step
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

3. Install the requirements
    ```{python}
        pip install -r requirements.txt 
    ```

4. Run the quantization. In our case we will run Falcon optimization. The script will download the model, run the quantization and save the results.

NOTE: This step can take a while depending on your hardware specifications.

    ```{python}
        python run_clm_no_trainer.py \
            --model tiiuae/falcon-7b-instruct \
            --quantize \
            --sq \
            --alpha 0.5 \
            --output_dir "saved_results" 
    ```

# OPTIONAL If you have AWS ECR

# Deploy it on Kubernetes

Create a network Load balancer

kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller/crds?ref=master"
helm repo add eks https://aws.github.io/eks-charts
helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
  --set clusterName=kubecon_langchain \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller


  TO CONNECT WITH THE ECT TO EKS
  export KUBECONFIG=/Users/emlanza/Library/CloudStorage/OneDrive-IntelCorporation/Technical/S2E/kubeconfig-kubecon.yaml
  export HTTPS_PROXY=http://proxy-chain.intel.com:912
export NO_PROXY=localhost,127.0.0.1,10.96.0.0/12,192.168.99.0/24,192.168.39.0/24

# FOR ECR Update keys 
kubectl create secret docker-registry ecr-secret \
  --docker-server=902415107800.dkr.ecr.us-east-1.amazonaws.com \
  --docker-username=AWS \
  --docker-password=$(aws ecr get-login-password --region us-east-1) 

# INSTALL THE NGNIX INGRESS CONTROLLER
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace --set controller.hostPort.enabled=true

# STEPS FROM 
https://aws.amazon.com/blogs/containers/exposing-kubernetes-applications-part-3-nginx-ingress-controller/

# FORWARDING A LA PC PARA QUE PUEDA CORRERLO LOCAL
#Make both ports forwared

kubectl port-forward -n kube-system svc/ingress-nginx-controller 8000:80

to test 
kubectl port-forward -n default pod/chat-backend-deployment-8595df5f46-cjqh5 8090:5000

# RUN INGRESS

# RUN PODS

# DELPLY PODS

# TEST INTERNALLY
# OPTIMIZATION 
git clone https://github.com/intel/intel-extension-for-transformers.git

cd examples/huggingface/pytorch/text-generation/quantization

python3 -m venv env_optim

source env_optim/bin/activate

pip install -r requirements.txt

Perfom the optimization

# Steps to create langserve
## 1 Install langchain-cli, this will enable you to use the cli and install langchain templates easily

## 2 There ara multiple templates with examples,in this case we will start with a clean environme but the tempalte will generate for us the files needed 

langchain app new chat-local 

It generates the files we need:
Important thing to mention is that it's using langserve api, which will make it easier











