# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/app/

COPY requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt &&\
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY ./llama2.py ./llama2.py

CMD ["python","llama2.py"]