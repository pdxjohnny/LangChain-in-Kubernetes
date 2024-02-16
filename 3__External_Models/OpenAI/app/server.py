from fastapi import FastAPI
from fastapi.responses import RedirectResponse
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
import os

app = FastAPI()
# Set up CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to the specific origin of your frontend in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

model = ChatOpenAI(openai_api_key="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")

add_routes(
    app,
    model,
    path="/openai_api",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=4000)
