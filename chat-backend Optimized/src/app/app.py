from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from src.chat.model import chain


app = FastAPI()

DB_FAISS_PATH = '/usr/app/src/chat/vectorstore/db_faiss'

test = chain(DB_FAISS_PATH)

# Set up CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origin of your frontend in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ws", response_class=PlainTextResponse)
async def process_text_data(request: Request):
    try:
        prompt_text = await request.body()

        print("Received Data:", prompt_text)

        # Send text to be inferred
        answer_from_model = test.inference(prompt_text.decode("utf-8"))
        # print(answer_from_model['result'])

        return answer_from_model['result']

    except Exception as e:
        print("Error:", str(e))

