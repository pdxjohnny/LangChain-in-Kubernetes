from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from langserve import RemoteRunnable
from langchain.prompts.chat import ChatPromptTemplate
from pydantic import BaseModel

class Data(BaseModel):
    question: str

class CustomMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        self.openai_llm = RemoteRunnable("http://localhost:8000/openai_api")
        super().__init__(app)

    async def dispatch(self, request, call_next):
        try:
            if request.url.path == '/api':
                data = await request.json()  # Get JSON data from request body
                question = data.get("question")  # Extract 'question' from JSON data

                llama_chain = RemoteRunnable("http://localhost:8000/llama_chain")
                result = llama_chain.invoke({"question": question})  # Pass the extracted question
                response = PlainTextResponse(result)
            elif request.url.path == '/apiopenai':
                data = await request.json()
                user_question= str(data.get("question"))
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a highly educated person who loves to use big words. "
                    + "You are also concise. Never answer in more than three sentences."),
                    ("human", user_question),
                ]).format_messages()
                print("llego aca")
                result = self.openai_llm.invoke(prompt)
                response = PlainTextResponse(result.content)
            else:
                response = await call_next(request)
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        return response

app = FastAPI()

# Allow all origins with necessary methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.add_middleware(CustomMiddleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
