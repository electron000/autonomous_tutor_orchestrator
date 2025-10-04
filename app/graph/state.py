# app/graph/state.py
import operator
from typing import TypedDict, Annotated, List, Optional, Any
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        messages: The list of messages in the conversation.
        user_info: Personalization context for the student.
        selected_tool: The name of the tool selected by the router.
        tool_parameters: The parameters extracted for the selected tool.
        missing_parameters: List of required parameters that are missing.
        clarification_question: The question to ask the user for missing info.
        tool_response: The response from the external tool.
        final_output: The final user-facing output.
        error: Any error message generated during the workflow.
    """
    messages: List[BaseMessage]
    user_info: dict
    selected_tool: Optional[str]
    tool_parameters: Optional[dict]
    missing_parameters: Optional[List[str]]
    clarification_question: Optional[str]
    tool_response: Optional[Any]
    final_output: Optional[str]
    error: Optional[str]