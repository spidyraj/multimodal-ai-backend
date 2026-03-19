import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_response(user_input):
    try:
        logger.info(f"Processing request: {user_input[:100]}...")
        
        if not GROQ_API_KEY or GROQ_API_KEY == "your_actual_key_here":
            logger.error("Invalid or missing Groq API key")
            return "Error: Invalid API key. Please configure your Groq API key in .env file."
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_input}
            ]
        }
        
        logger.info("Making request to Groq API...")
        response = requests.post(
            url, 
            headers=headers, 
            json=data, 
            timeout=10.0
        )
        
        logger.info(f"Groq API response status: {response.status_code}")
        
        if response.status_code == 401:
            logger.error("Invalid API key")
            return "Error: Invalid API key. Please check your Groq API key."
        
        elif response.status_code == 429:
            logger.error("Rate limit exceeded")
            return "Error: Rate limit exceeded. Please try again in a moment."
        
        elif response.status_code != 200:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return f"Error: API returned status {response.status_code}. {response.text[:200]}"
        
        response_data = response.json()
        logger.info("Successfully received response from Groq API")
        
        return response_data["choices"][0]["message"]["content"]
        
    except requests.exceptions.Timeout:
        logger.error("Request timeout after 10 seconds")
        return "Error: Request timeout. The AI service took too long to respond. Please try again."
    
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
        return "Error: Cannot connect to AI service. Please check your internet connection."
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return f"Error: Network error occurred. {str(e)}"
    
    except (KeyError, IndexError) as e:
        logger.error(f"Response parsing error: {str(e)}")
        return "Error: Invalid response format from AI service."
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Error: An unexpected error occurred. Please try again."
