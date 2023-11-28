FROM python:3.11.2

WORKDIR /usr/app/src

COPY Data/* /usr/app/src/Data 
COPY requirements.txt /usr/app/src/
COPY ingest.py /usr/app/src/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
RUN pwd

# Create the Vector database
CMD ["python","ingest.py --folder /usr/app/src/Data"]

