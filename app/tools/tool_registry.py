# app/tools/tool_registry.py
import os
import json
from typing import Any, Dict, List, Literal, Optional, Type
from pydantic import BaseModel, Field, create_model
from langchain.tools import StructuredTool

# --- Helper Functions to Build Pydantic Models from JSON Schema ---

JSON_TYPE_TO_PYTHON_TYPE = {
    "string": str,
    "integer": int,
    "number": float,
    "boolean": bool,
}

def create_pydantic_model_from_schema(
    schema: Dict[str, Any], model_name: str
) -> Type:
    """Dynamically creates a Pydantic model from a JSON schema's properties."""
    fields = {}
    # Corrected line: Default to an empty list if 'required' key is missing.
    # This fixes the TypeError during recursion.
    required_fields = schema.get("required", [])

    for name, prop in schema.get("properties", {}).items():
        description = prop.get("description")
        is_required = name in required_fields
        
        field_type = Any
        json_type = prop.get("type")

        if "enum" in prop:
            # Create a Literal type from the enum list
            field_type = Literal[tuple(prop["enum"])]
        elif json_type == "object":
            # Recursively create a nested model for the object type
            nested_model_name = f"{model_name}_{name.capitalize()}"
            field_type = create_pydantic_model_from_schema(prop, nested_model_name)
        elif json_type == "array":
            items = prop.get("items", {})
            item_type_str = items.get("type")
            if items.get("enum"):
                item_type = Literal[tuple(items["enum"])]
            elif item_type_str == "object":
                nested_model_name = f"{model_name}_{name.capitalize()}Item"
                item_type = create_pydantic_model_from_schema(items, nested_model_name)
            else:
                item_type = JSON_TYPE_TO_PYTHON_TYPE.get(item_type_str, Any)
            field_type = List[item_type]
        else:
            field_type = JSON_TYPE_TO_PYTHON_TYPE.get(json_type, Any)

        if not is_required:
            field_type = Optional[field_type]

        # Use Field to include the description
        default_value = ... if is_required else None
        fields[name] = (field_type, Field(default=default_value, description=description))

    return create_model(model_name, **fields)

# --- Main Function to Load Tools ---

def load_tools_from_directory(directory_path: str) -> Dict:
    """Loads all tool definitions from JSON files in a directory."""
    tools = {}
    if not os.path.exists(directory_path):
        print(f"Warning: Tool definition directory not found at '{directory_path}'")
        return {}

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r") as f:
                schema = json.load(f)

                # Use filename without extension as the primary tool name
                tool_name = filename.replace(".json", "")
                # Use schema's title for description, fallback to a default
                tool_description = schema.get("description", f"A tool named {tool_name}.")
                
                # Dynamically create the Pydantic model for arguments
                args_schema = create_pydantic_model_from_schema(schema, f"{tool_name}Input")

                # --- MODIFIED: Added detailed comment to placeholder function ---
                def placeholder_func(**kwargs):
                    """
                    This is a placeholder function. The StructuredTool is used here only
                    to hold the tool's name, description, and args_schema. The actual
                    tool execution is handled by the 'execute_tool' node in the graph,
                    which makes an external API call.
                    """
                    return f"{tool_name} called with: {kwargs}"

                # Create the StructuredTool
                structured_tool = StructuredTool.from_function(
                    func=placeholder_func,
                    name=tool_name,
                    description=tool_description,
                    args_schema=args_schema,
                )
                tools[tool_name] = structured_tool
    return tools

# --- Initialize the Tool Registry ---

# Get the absolute path to the 'tool_definitions' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
definitions_dir = os.path.join(current_dir, "tool_definitions")

# Load the tools and create the registry
tool_registry = load_tools_from_directory(definitions_dir)

# This print statement is helpful for debugging to confirm tools are loaded
if tool_registry:
    print(f"Successfully loaded {len(tool_registry)} tools: {list(tool_registry.keys())}")
else:
    print("Warning: No tools were loaded from the tool_definitions directory.")