# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/app/src

# Copy the application files into the container
COPY ./Data/ ./Data
COPY requirements.txt ./
COPY ingest.py ./
COPY model.py ./

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN chmod +x ingest.py

#Specify the command to run on container start

CMD python ingest.py --folder /usr/app/src/Data  && python model.py

EXPOSE 8000
RUN echo "Vectordatabase created"



