# mock_services/mock_notes_service.py
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

class ChatHistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class NoteMakerRequest(BaseModel):
    """
    This model now exactly matches the JSON schema for the note_maker_tool.
    """
    user_info: UserInfo
    chat_history: List[ChatHistoryItem]
    topic: str
    subject: str
    note_taking_style: Literal["outline", "bullet_points", "narrative", "structured"]
    include_examples: Optional[bool] = True
    include_analogies: Optional[bool] = False


@app.post("/generate-notes")
async def generate_notes(request: NoteMakerRequest):
    """
    A mock endpoint for the Note Maker Tool that now accepts the full
    input schema and returns a response matching the detailed output schema.
    """
    
    # Dynamically generate content based on the request
    note_sections = [
        {
            "title": f"Introduction to {request.topic}",
            "content": f"This section provides a foundational overview of {request.topic}, tailored for a {request.user_info.grade_level} grade level.",
            "key_points": [
                f"Core definition of {request.topic}",
                "Primary components and functions."
            ],
            "examples": [],
            "analogies": []
        },
        {
            "title": "Key Processes",
            "content": "A detailed look into the key processes involved.",
            "key_points": [
                "Step-by-step process walkthrough.",
                "Interaction with other systems."
            ],
            "examples": [],
            "analogies": []
        }
    ]

    # Conditionally add examples and analogies based on the request
    if request.include_examples:
        note_sections[0]["examples"].append(f"A common example of {request.topic} is when X happens, which results in Y.")
    
    if request.include_analogies:
        note_sections[1]["analogies"].append(f"Think of {request.topic} like a complex machine with interconnected parts.")

    # Build the full response object according to the specified schema
    return {
        "topic": request.topic,
        "title": f"Structured Notes on {request.topic}",
        "summary": f"A brief overview of {request.topic} in {request.subject}, prepared for {request.user_info.name}. This summary is based on your stated mastery level: '{request.user_info.mastery_level_summary}'.",
        "note_sections": note_sections,
        "key_concepts": [
            "Primary Concept A",
            "Secondary Concept B",
            "Tertiary Concept C"
        ],
        "connections_to_prior_learning": [
            f"Connects to your previous study of related topics in {request.subject}."
        ],
        "visual_elements": [
            {"type": "diagram", "description": f"A flowchart of the {request.topic} process."}
        ],
        "practice_suggestions": [
            "Try to draw the main cycle from memory.",
            "Explain the concept to a friend in your own words."
        ],
        "source_references": [
            "Textbook Chapter 4",
            "Online Educational Resource URL"
        ],
        "note_taking_style": request.note_taking_style
    }