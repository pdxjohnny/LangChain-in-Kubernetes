from fastapi import FastAPI,HTTPException
from pydantic import BaseModel 
from src.chat.model import chain
import logging

app = FastAPI()
#LOCAL
DB_FAISS_PATH='/Users/emlanza/Library/CloudStorage/OneDrive-IntelCorporation/Technical/S2E/Events/Kubecon EU 2024/LangChain-in-Kubernetes/chat-backend/src/chat/vectorstore/db_faiss/'
#DB_FAISS_PATH = '/usr/app/src/chat/vectorstore/db_faiss'
logger = logging.getLogger(__name__)

class text_data(BaseModel):
    prompt_text : str

test=chain(DB_FAISS_PATH)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to limit origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.DEBUG)

@app.post("/ws")
async def process_text_data(request: text_data):
    try:
        # Get the raw bytes from the request body
        raw_data = await request.body()
        
        # Decode the raw bytes into a string
        text_data = raw_data.decode("utf-8")

        logger.info("Received Data: %s", text_data)

        print("Received Data:", text_data)  # Add this line for logging

        #Send text to be inferenced
        answer_from_model = test.inference(text_data)

        return (answer_from_model['result'])
    except Exception as e:
        print("Error:", str(e))  # Add this line for logging
        raise HTTPException(status_code=500, detail=str(e))