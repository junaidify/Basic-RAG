from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def model_call():
    result = client.chat.completions.create(
        model = "qwen/qwen3.8-27b", 
        messages = [
            {
                "role" : "system", 
                "content" : "Act as Senior Ai engineer"
            }, 
            {
                "role" : "user", 
                "content": "Explain about RAG pipeline basics?"
            }
        ],
        stream = True, 
        max_completion_tokens=500
    
    )

    for chunk in result:
        print(chunk.choices[0].delta.content, end="")
    
