# app/core/llm.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

def get_llm():
    """Initializes and returns the Gemini Flash LLM."""
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    # Explicitly pass the API key to the constructor to ensure it's used.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=settings.GOOGLE_API_KEY
    )
    return llm

# Create a single, reusable instance of the LLM
llm = get_llm()