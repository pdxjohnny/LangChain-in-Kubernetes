from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from src.chat.model import chain


app = FastAPI()

DB_FAISS_PATH = '/usr/app/src/chat/vectorstore/db_faiss'
name_model = "Llama"
test = chain(DB_FAISS_PATH,name_model)

# Set up CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origin of your frontend in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api", response_class=PlainTextResponse)
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


### TODO, ADD MULTIPLE /API/LLAMA OR API/FALCON, TO ALLOW THE FRONT END TO SELECT WHICH MODEL TO USE. FALCON OR LLAMA
