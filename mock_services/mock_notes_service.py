# mock_services/mock_notes_service.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Literal

app = FastAPI()

# A simplified input model to accept the request
class NoteMakerRequest(BaseModel):
    topic: str
    subject: str

class NoteSection(BaseModel):
    title: str
    content: str
    key_points: List[str]

@app.post("/generate-notes")
async def generate_notes(request: NoteMakerRequest):
    """
    A mock endpoint for the Note Maker Tool.
    It returns a pre-defined, valid JSON response.
    """
    return {
        "topic": request.topic,
        "title": f"Comprehensive Notes on {request.topic}",
        "summary": f"This document contains a structured overview of {request.topic} in the context of {request.subject}.",
        "note_sections": [
            {
                "title": "Introduction",
                "content": f"An introduction to the fundamental concepts of {request.topic}.",
                "key_points": ["Key Point 1", "Key Point 2"]
            },
            {
                "title": "Core Concepts",
                "content": "A detailed breakdown of the main principles.",
                "key_points": ["Core detail A", "Core detail B"]
            }
        ],
        "key_concepts": ["Concept Alpha", "Concept Beta"],
        "note_taking_style": "structured"
    }
