# mock_services/mock_concept_service.py
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

class ConceptRequest(BaseModel):
    """
    This model now exactly matches the JSON schema for the concept_explainer_tool.
    """
    user_info: UserInfo
    chat_history: List[ChatHistoryItem]
    concept_to_explain: str
    current_topic: str
    desired_depth: Literal["basic", "intermediate", "advanced", "comprehensive"]


@app.post("/explain-concept")
async def explain_concept(request: ConceptRequest):
    """
    A mock endpoint for the Concept Explainer Tool that now accepts the full
    input schema and returns a response matching the detailed output schema.
    """
    
    # Dynamically generate content based on the request
    explanation_text = (
        f"Here is a {request.desired_depth} explanation of '{request.concept_to_explain}' for {request.user_info.name}. "
        f"Considering your mastery level is '{request.user_info.mastery_level_summary}', we'll start with the core ideas. "
        f"In the context of {request.current_topic}, the concept is defined by..."
    )

    # Build the full response object according to the specified schema
    return {
        "explanation": explanation_text,
        "examples": [
            f"A practical example of {request.concept_to_explain} is...",
            "Another way to see it is in action is when..."
        ],
        "related_concepts": [
            "A closely related concept is...",
            "This also connects to the idea of..."
        ],
        "visual_aids": [
            f"A helpful diagram for understanding {request.concept_to_explain} would be a flowchart.",
            f"A mind map connecting the main parts of {request.concept_to_explain}."
        ],
        "practice_questions": [
            f"Can you explain {request.concept_to_explain} in your own words?",
            "How does this concept apply to a real-world problem?"
        ],
        "source_references": [
            "Your textbook, Chapter 5, Section 2.",
            "Khan Academy article on the topic."
        ]
    }