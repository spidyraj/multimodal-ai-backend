# Multimodal AI Backend

A FastAPI backend for multimodal AI chatbot with Groq API integration.

## Setup Instructions

### 1. Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Edit `.env` file and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 4. Run the Server
```bash
uvicorn main:app --reload
```

### 5. Test the API
- Open http://127.0.0.1:8000/docs for interactive API documentation
- Test POST /chat endpoint with JSON:
```json
{
  "message": "Explain blockchain simply"
}
```

## API Endpoints

- `GET /` - Health check
- `POST /chat` - Chat with AI assistant

## Project Structure
```
├── main.py              # FastAPI application
├── llm_service.py       # Groq API integration
├── requirements.txt     # Python dependencies
├── .env                # Environment variables
└── README.md           # This file
```

## Next Steps
Ready for Step 2: RAG implementation with FAISS + LangChain
