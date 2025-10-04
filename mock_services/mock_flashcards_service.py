# mock_services/mock_flashcards_service.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

app = FastAPI()

# --- Define Pydantic models to match the detailed input schema ---

class UserInfo(BaseModel):
    user_id: str
    name: str
    grade_level: str
    learning_style_summary: str
    emotional_state_summary: str
    mastery_level_summary: str

class FlashcardRequest(BaseModel):
    """
    This model now exactly matches the JSON schema for the flashcard_generator_tool.
    """
    user_info: UserInfo
    topic: str
    count: int = Field(..., ge=1, le=20) # Enforce min/max constraints
    difficulty: Literal["easy", "medium", "hard"]
    subject: str
    include_examples: Optional[bool] = True


@app.post("/generate-flashcards")
async def generate_flashcards(request: FlashcardRequest):
    """
    A mock endpoint for the Flashcard Generator Tool that now accepts the full
    input schema and returns a response matching the detailed output schema.
    """
    
    flashcards = []
    # Dynamically generate flashcard content based on the request
    for i in range(1, request.count + 1):
        card = {
            "title": f"{request.topic} - Key Term {i}",
            "question": f"What is a core concept of {request.topic} related to {request.subject}?",
            "answer": f"This is the detailed answer for the concept, tailored for a {request.difficulty} level.",
            "example": None # Initialize example as None
        }
        # Conditionally add an example if requested
        if request.include_examples:
            card["example"] = f"A simple example of this is when..."
        
        flashcards.append(card)
        
    # Build the full response object according to the specified schema
    return {
        "flashcards": flashcards,
        "topic": request.topic,
        "adaptation_details": f"Generated {request.count} flashcards for {request.user_info.name} at a {request.difficulty} level, adapting to their '{request.user_info.emotional_state_summary}' state.",
        "difficulty": request.difficulty
    }

