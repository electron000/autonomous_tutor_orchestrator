# mock_services/mock_flashcards_service.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Literal

app = FastAPI()

class FlashcardRequest(BaseModel):
    topic: str
    count: int
    difficulty: str

class Flashcard(BaseModel):
    title: str
    question: str
    answer: str

@app.post("/generate-flashcards")
async def generate_flashcards(request: FlashcardRequest):
    """
    A mock endpoint for the Flashcard Generator Tool.
    It returns a pre-defined, valid JSON response based on the request.
    """
    flashcards = []
    for i in range(1, request.count + 1):
        flashcards.append({
            "title": f"{request.topic} ({request.difficulty})",
            "question": f"What is a key aspect of {request.topic}? (Card {i})",
            "answer": f"This is the detailed answer for flashcard {i} about {request.topic}."
        })
