from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import httpx
import datetime
import json
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGODB_URI)
db = client["voice_assistant"]
interactions_collection = db["interactions"]

# Groq Cloud API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class VoiceInput(BaseModel):
    text: str
    user_id: str = "anonymous"

async def get_intent_and_response(text: str):
    """
    Uses Groq Cloud API to determine intent and generate a response.
    """
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        messages = [{"role": "user", "content": text}]
        
        tools = [{
            "type": "function",
            "function": {
                "name": "determine_intent_and_respond",
                "description": "Determine intent and generate a response.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "intent": {"type": "string", "description": "Intent of the query."},
                        "response": {"type": "string", "description": "Generated response."}
                    },
                    "required": ["intent", "response"]
                }
            }
        }]

        data = {
            "model": "llama3-8b-8192",
            "messages": messages,
            "tools": tools,
            "tool_choice": {"type": "function", "function": {"name": "determine_intent_and_respond"}}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, headers=headers, json=data, timeout=10.0)

        response.raise_for_status()

        response_json = response.json()
        
        if "choices" not in response_json or not response_json["choices"]:
            raise HTTPException(status_code=500, detail="Unexpected Groq API response format.")

        response_message = response_json["choices"][0]["message"]

        if "tool_calls" in response_message and response_message["tool_calls"]:
            args = json.loads(response_message["tool_calls"][0]["function"]["arguments"])
            return args.get("intent"), args.get("response")
        
        return None, response_message.get("content", "I'm sorry, I couldn't understand that.")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code if e.response else 500, detail=f"Groq API error: {str(e)}")
    except (json.JSONDecodeError, KeyError) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing Groq response: {str(e)}, Raw Response: {response.text if 'response' in locals() else 'No response'}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/process-voice")
async def process_voice(input_data: VoiceInput):
    intent, response_text = await get_intent_and_response(input_data.text)

    interaction = {
        "user_id": input_data.user_id,
        "input_text": input_data.text,
        "intent": intent,
        "response": response_text,
        "timestamp": datetime.datetime.utcnow()
    }

    try:
        await interactions_collection.insert_one(interaction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"response": response_text}

