# app/api/endpoints/orchestrator.py
from fastapi import APIRouter, HTTPException
# --- REVERTED: Remove ChatMessage, we only need these ---
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List

from app.schemas.api_schemas import ChatRequest, ChatResponse, ChatHistoryItem
from app.graph.workflow import app_graph

router = APIRouter()

# --- REVERTED: Go back to using AIMessage ---
def _convert_history_to_messages(history: List[ChatHistoryItem]) -> List[BaseMessage]:
    """Converts a list of ChatHistoryItem models to a list of LangChain message objects."""
    messages = []
    for item in history:
        if item.role == "user":
            messages.append(HumanMessage(content=item.content))
        elif item.role == "assistant":
            # Go back to using AIMessage
            messages.append(AIMessage(content=item.content))
    return messages

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Convert the chat history from the request into LangChain message objects
    messages = _convert_history_to_messages(request.chat_history)
    # Add the latest user message
    messages.append(HumanMessage(content=request.message))
    
    initial_state = {
        "messages": messages,
        "user_info": request.user_info,
    }

    try:
        # Asynchronously stream the events from the graph to get the final state
        final_state = None
        async for item in app_graph.astream(initial_state):
            final_state = item

        # The final state is the last item yielded by the stream
        if not final_state:
            raise HTTPException(status_code=500, detail="Orchestrator did not produce a final state.")

        # Get the name of the last node that ran (it's the only key in the dict)
        last_node_name = list(final_state.keys())[0]
        # Get the dictionary of values produced by that last node
        final_values = final_state[last_node_name]
        
        response_message = final_values.get("final_output") or final_values.get("clarification_question")

        if not response_message:
            # Handle cases where there's an error or no output
            error_message = final_values.get("error", "Orchestrator failed to produce a response.")
            raise HTTPException(status_code=500, detail=error_message)

        return ChatResponse(response=response_message, conversation_id=request.conversation_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")