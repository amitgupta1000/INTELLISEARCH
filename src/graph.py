# graph.py
# This file defines the LangGraph workflow.

import logging

# Try to import LangGraph; provide a minimal fallback for static linting/runtime without the package
try:
    from langgraph.graph import StateGraph, START, END, add_messages
except Exception:
    logging.warning("langgraph.graph not available; using fallback StateGraph for static checks.")
    # Minimal fallback implementation so other modules can import graph during lint/static analysis
    START = "__START__"
    END = "__END__"
    add_messages = None
    class StateGraph:
        def __init__(self, state_type=None):
            self.nodes = {}
        def add_node(self, name, func):
            self.nodes[name] = func
        def add_edge(self, a, b):
            pass
        def add_conditional_edges(self, node, route_fn, mapping):
            pass
        def compile(self):
            logging.info("Fallback StateGraph.compile() called — no-op.")
            return None

from typing import TypedDict, Optional, List, Dict, Any # Import necessary types
from .conditions import (
    should_continue_search,
    should_terminate_search,
    should_continue_approval,
    should_terminate_approval
)
# Import nodes and AgentState from nodes.py
try:
    from .nodes import (
        AgentState,
        create_queries,
        user_approval_for_queries,
        evaluate_search_results,
        extract_content,
        embed_index_and_extract,
        AI_evaluate,
        choose_report_type,
        write_report,
    )
except ImportError as e:
    import logging
    logging.exception("Error importing nodes: %s. Cannot define graph.", e)
    
# Initialize StateGraph
workflow = StateGraph(AgentState)

# Add nodes
# Assuming all imported node functions are async
if 'create_queries' in locals():
    workflow.add_node("create_queries", create_queries)
if 'user_approval_for_queries' in locals():
    workflow.add_node("user_approval", user_approval_for_queries)
if 'evaluate_search_results' in locals():
    workflow.add_node("evaluate_search_results", evaluate_search_results)
if 'extract_content' in locals():
    workflow.add_node("extract_content", extract_content)
if 'embed_index_and_extract' in locals():
    workflow.add_node("embed_index_and_extract", embed_index_and_extract)
if 'AI_evaluate' in locals():
    workflow.add_node("AI_evaluate", AI_evaluate)
if 'choose_report_type' in locals():
    workflow.add_node("choose_report_type", choose_report_type)
if 'write_report' in locals():
    workflow.add_node("write_report", write_report)

# Add edges - check if nodes were successfully added before adding edges
if all(node_name in workflow.nodes for node_name in ["create_queries", "user_approval"]):
    workflow.add_edge(START, "create_queries")
    workflow.add_edge("create_queries", "user_approval")


from .conditions import route_user_approval

workflow.add_conditional_edges(
    "user_approval",
    route_user_approval,
    {
        "create_queries": "create_queries",
        "evaluate_search_results": "evaluate_search_results",
        "choose_report_type": "choose_report_type"
    }
)

# Add sequential edges
if "evaluate_search_results" in workflow.nodes and "extract_content" in workflow.nodes:
    workflow.add_edge("evaluate_search_results", "extract_content")

if "extract_content" in workflow.nodes and "embed_index_and_extract" in workflow.nodes:
    workflow.add_edge("extract_content", "embed_index_and_extract")

if "embed_index_and_extract" in workflow.nodes and "AI_evaluate" in workflow.nodes:
    workflow.add_edge("embed_index_and_extract", "AI_evaluate")


from .conditions import route_ai_evaluate

workflow.add_conditional_edges(
    "AI_evaluate",
    route_ai_evaluate,
    {
        "evaluate_search_results": "evaluate_search_results",
        "choose_report_type": "choose_report_type"
    }
)

# Add edge from choose_report_type to write_report
if "choose_report_type" in workflow.nodes and "write_report" in workflow.nodes:
    workflow.add_edge("choose_report_type", "write_report")

# Edge to END from write_report
if "write_report" in workflow.nodes:
    workflow.add_edge("write_report", END)


# Compile the workflow if nodes were successfully added
try:
    app = workflow.compile()
    logging.info("LangGraph workflow compiled successfully.")
except Exception as e:
    logging.exception("Error compiling LangGraph workflow: %s", e)
    app = None # Set app to None if compilation fails
