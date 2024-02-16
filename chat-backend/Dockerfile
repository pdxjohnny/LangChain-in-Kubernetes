# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory in the container
#WORKDIR /usr/app/

COPY requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./src ./src/
COPY ./src/main.py ./main.py
COPY ./src/app/app.py ./app.py



# Set a default port as an environment variable
ENV PORT=8000

# Expose the port
EXPOSE $PORT

CMD ["python","main.py"]