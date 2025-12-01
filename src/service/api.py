from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "Hello from vvalkman API"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # Placeholder for LLM integration
    return {"response": f"You said: {request.message}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
