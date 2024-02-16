from fastapi import FastAPI, Request, Request,HTTPException
from langserve import RemoteRunnable
from langchain.prompts.chat import ChatPromptTemplate
from fastapi.responses import PlainTextResponse
from fastapi import Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi import Header

class Data(BaseModel):
    question: str

app = FastAPI()

# Allow all origins with necessary methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  # Add comma here
    allow_headers=["*"],  # Add comma here
    allow_credentials=False,
)

openai_llm = RemoteRunnable("http://localhost:8000/openai_api")


@app.post("/api", response_class=PlainTextResponse)
async def process_text_data(request: Request):

    try:
        data = await request.json()  # Get JSON data from request body
        question = data.get("question")  # Extract 'question' from JSON data
        llama_chain = RemoteRunnable("http://localhost:8000/llama_chain")
        print("ESTA ADENTRO")
        result = llama_chain.invoke({"question": question})  # Pass the extracted question
        return result
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    
 
@app.post("/apiopenai")
async def process_text_data(question: Data,user_agent: str = Header(None)):
    try:
        print("Entering try block...")
        user_question= str(question.question)
        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a highly educated person who loves to use big words. "
                    + "You are also concise. Never answer in more than three sentences.",
                ),
                ("human", user_question),
            ]       
        ).format_messages()     
        
                # Pass the extracted question
        print("entra")
        print("User-Agent:", user_agent) 
        result=openai_llm.invoke(prompt)
        print("salio")
        print(result.content)
        
        return result.content
    
    except Exception as e:
        print("Entering ERROR block...")
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

 


if __name__=='__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)