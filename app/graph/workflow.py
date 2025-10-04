# app/graph/workflow.py
from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.graph.nodes import (
    route_tool,
    extract_parameters,
    clarify_parameters,
    execute_tool,
    format_response,
)

# Define the conditional routing logic
def should_continue(state: GraphState):
    if state.get("error"):
        return "end"
    if state.get("selected_tool") is None:
        return "end"
    return "extract_parameters"

def after_extraction(state: GraphState):
    if state.get("error"):
        return "end"
    if state.get("missing_parameters"):
        return "clarify_parameters"
    return "execute_tool"

def after_execution(state: GraphState):
    if state.get("error"):
        return "end"
    return "format_response"

# Define a new graph
workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("route_tool", route_tool)
workflow.add_node("extract_parameters", extract_parameters)
workflow.add_node("clarify_parameters", clarify_parameters)
workflow.add_node("execute_tool", execute_tool)
workflow.add_node("format_response", format_response)

# Build the graph
workflow.set_entry_point("route_tool")

# Use the corrected 'add_conditional_edges' method
workflow.add_conditional_edges(
    "route_tool",
    should_continue,
    {
        "extract_parameters": "extract_parameters",
        "end": END,
    },
)

# Use the corrected 'add_conditional_edges' method
workflow.add_conditional_edges(
    "extract_parameters",
    after_extraction,
    {
        "clarify_parameters": "clarify_parameters",
        "execute_tool": "execute_tool",
        "end": END,
    },
)

workflow.add_edge("clarify_parameters", END)

# Use the corrected 'add_conditional_edges' method
workflow.add_conditional_edges(
    "execute_tool",
    after_execution,
    {
        "format_response": "format_response",
        "end": END,
    }
)

workflow.add_edge("format_response", END)

# Compile the graph
app_graph = workflow.compile()