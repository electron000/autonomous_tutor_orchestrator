# app/graph/nodes.py
import httpx
import json
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Literal

# Import the centralized LLM instance
from app.core.llm import llm
from app.graph.state import GraphState
from app.tools.tool_registry import tool_registry

# --- 1. ROUTER NODE (Unchanged) ---

class Route(BaseModel):
    """Select the next step to take based on the user's query."""
    tool_name: str = Field(
        description="The name of the tool to use, which must be one of the tools provided or 'NoTool'."
    )

def route_tool(state: GraphState) -> dict:
    """Analyzes the user's latest message to decide which tool to use."""
    messages = state["messages"]
    last_message_content = messages[-1].content

    tool_names = ", ".join(tool_registry.keys())
    tool_descriptions = "\n".join(
        [f"- {name}: {tool.description}" for name, tool in tool_registry.items()]
    )

    prompt_template = f"""You are an expert at routing a user's request to the correct educational tool.
Based on the user's last message, select the most appropriate tool from the following list:
{tool_descriptions}

User message: "{last_message_content}"

You must respond with one of the following tool names: {tool_names}, or 'NoTool' if no tool is a good match.
"""

    structured_llm = llm.with_structured_output(Route)

    try:
        route_decision = structured_llm.invoke(prompt_template)
        if route_decision.tool_name == "NoTool" or route_decision.tool_name not in tool_registry:
            return {"selected_tool": None, "final_output": "I can't directly answer that, but I can help with other educational tools. What would you like to do?"}
        else:
            return {"selected_tool": route_decision.tool_name}
    except Exception as e:
        return {"selected_tool": None, "error": f"Router failed: {str(e)}"}

# --- 2. PARAMETER EXTRACTION NODE (FIXED) ---

def extract_parameters(state: GraphState) -> dict:
    """Extracts parameters for the selected tool from the conversation."""
    selected_tool_name = state["selected_tool"]
    if not selected_tool_name:
        return {}

    tool_schema = tool_registry[selected_tool_name].args_schema
    structured_llm = llm.with_structured_output(tool_schema)

    # --- FIX APPLIED HERE: Added a specific instruction to the prompt ---
    # Create a detailed prompt template to guide the LLM
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an expert at extracting parameters for a given tool from a conversation. "
         "Based on the following conversation and user information, extract the required parameters for the '{tool_name}' tool.\n"
         "IMPORTANT: When extracting the 'chat_history' parameter, you MUST ensure that the 'role' for any AI-generated message is the string 'assistant'. Do not use 'model' or 'ai'.\n\n"
         "User Information:\n{user_info_str}"
        ),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = prompt | structured_llm

    try:
        extracted_params = chain.invoke({
            "tool_name": selected_tool_name,
            "user_info_str": json.dumps(state["user_info"].model_dump(), indent=2),
            "messages": state["messages"]
        })

        required_fields = {name for name, field in tool_schema.__fields__.items() if field.is_required()}
        provided_params = {k for k, v in extracted_params.dict().items() if v is not None}

        missing = list(required_fields - provided_params)

        if missing:
            return {"tool_parameters": extracted_params.dict(), "missing_parameters": missing}
        else:
            return {"tool_parameters": extracted_params.dict(), "missing_parameters": None}
    except Exception as e:
        return {"error": f"Parameter extraction failed: {str(e)}"}

# --- 3. CLARIFICATION NODE (Unchanged) ---

def clarify_parameters(state: GraphState) -> dict:
    """Generates a question to ask the user for missing parameters."""
    missing_params = state["missing_parameters"]
    if not missing_params:
        return {}

    existing_params = state.get("tool_parameters", {})

    prompt = f"""The user wants to use the '{state['selected_tool']}' tool.
We have already figured out these details: {existing_params}.
However, we are still missing some information.
Please formulate a friendly, single-sentence question to ask the user for the following missing parameter(s): {', '.join(missing_params)}.
Example: If 'difficulty' is missing, ask "What difficulty level would you like?"
"""

    try:
        clarification = llm.invoke(prompt).content
        return {"clarification_question": clarification, "final_output": clarification}
    except Exception as e:
        error_message = f"Failed to generate clarification question: {str(e)}"
        return {"error": error_message, "final_output": "I'm sorry, I had trouble understanding. Could you please provide more details?"}

# --- 4. TOOL EXECUTION NODE (Unchanged) ---

TOOL_ENDPOINTS = {
    "note_maker_tool": "http://localhost:8001/generate-notes",
    "flashcard_generator_tool": "http://localhost:8002/generate-flashcards",
    "concept_explainer_tool": "http://localhost:8003/explain-concept",
}

async def execute_tool(state: GraphState) -> dict:
    """Executes the selected tool by making an API call."""
    tool_name = state["selected_tool"]
    params = state["tool_parameters"]

    if not tool_name or not params:
        return {"error": "Tool name or parameters are missing for execution."}

    endpoint = TOOL_ENDPOINTS.get(tool_name)
    if not endpoint:
        return {"error": f"Endpoint for tool '{tool_name}' not found."}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(endpoint, json=params, timeout=30.0)
            response.raise_for_status()
            return {"tool_response": response.json()}
        except httpx.RequestError as e:
            return {"tool_response": None, "error": f"API request failed for {tool_name}: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"tool_response": None, "error": f"API call for {tool_name} returned status {e.response.status_code}: {e.response.text}"}

# --- 5. RESPONSE FORMATTING NODE (Unchanged) ---

def format_response(state: GraphState) -> dict:
    """Formats the raw tool response into a user-friendly message."""
    tool_response = state["tool_response"]
    tool_name = state["selected_tool"]

    if not tool_response:
        error = state.get("error", "Sorry, there was an error processing your request.")
        return {"final_output": error}

    prompt = f"""You are a helpful AI Tutor. The '{tool_name}' tool has just run and produced the following JSON output.
Please format this information into a friendly, clear, and helpful message for the student.
Do not just show the raw JSON. Summarize it and present it in a conversational way.

Tool Output:
```json
{json.dumps(tool_response, indent=2)}
```"""
    try:
        formatted_output = llm.invoke(prompt).content
        return {"final_output": formatted_output}
    except Exception as e:
        return {"final_output": f"Here is the result from the {tool_name}:\n\n{json.dumps(tool_response, indent=2)}"}