from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from llm_service import get_llm_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Multimodal AI Chatbot", version="1.0.0")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    logger.info("Health check requested")
    return {"message": "API is running", "status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        logger.info(f"Received chat request: {request.message[:100]}...")
        
        if not request.message or not request.message.strip():
            logger.warning("Empty message received")
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if len(request.message) > 10000:
            logger.warning("Message too long")
            raise HTTPException(status_code=400, detail="Message too long (max 10000 characters)")
        
        response = get_llm_response(request.message)
        
        if response.startswith("Error:"):
            logger.error(f"LLM service error: {response}")
            raise HTTPException(status_code=503, detail=response)
        
        logger.info("Successfully processed chat request")
        return {"response": response}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "multimodal-ai-backend"}
