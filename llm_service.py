import os
import requests
from dotenv import load_dotenv

# Load only for local (safe)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_response(user_input):
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found in environment variables."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)

        print("Groq response:", response.text)

        if response.status_code != 200:
            return f"Error: {response.text}"

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"