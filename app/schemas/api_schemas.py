# app/schemas/api_schemas.py
from pydantic import BaseModel, Field
from typing import List, Literal

# Define a model for a single chat history message
class ChatHistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str

# Define a model for the user_info object
class UserInfo(BaseModel):
    name: str
    grade_level: str
    learning_style_summary: str
    emotional_state_summary: str
    mastery_level_summary: str


class ChatRequest(BaseModel):
    """Request model for the /chat endpoint."""
    user_id: str
    conversation_id: str
    message: str
    # Use the strongly-typed models
    user_info: UserInfo
    chat_history: List[ChatHistoryItem]

class ChatResponse(BaseModel):
    """Response model for the /chat endpoint."""
    response: str
    conversation_id: str