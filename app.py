# app.py # This is the main execution file for your application.

import asyncio
import logging
from typing import Dict, Any, List

# Basic logging configuration in case setup.py didn't configure it
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# RunnableConfig is optional (depends on langchain_core availability)
try:
    from langchain_core.runnables import RunnableConfig
    config = RunnableConfig(recursion_limit=100)
except Exception:
    logging.debug("langchain_core.runnables not available; continuing without RunnableConfig.")
    config = None

# Import necessary components from your modules

try:
    import setup
    logging.info("setup.py imported and likely executed initial setup.")
except ImportError as e:
    logging.error(f"Could not import setup.py: {e}. Initial setup may be incomplete.")
    # Basic logging config if setup failed
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Import the compiled LangGraph application
    from src.graph import app 
except ImportError as e:
    logging.error(f"Could not import the LangGraph app from graph.py: {e}. Cannot run the workflow.")
    app = None # Set app to None if import fails

try:
    # Import AgentState for type hinting initial state
    from src.nodes import AgentState
except ImportError as e:
    logging.error(f"Could not import AgentState from nodes.py: {e}. Type hinting for initial state may be missing.")
    # Define a dummy AgentState if import fails, or handle gracefully
    AgentState = Dict[str, Any] # Fallback to a generic dictionary type hint


async def run_workflow(initial_query: str, reasoning_mode_flag: bool, prompt_type: str):
    """
    Runs the LangGraph workflow with an initial query.

    Args:
        initial_query: The user's initial research query.
    """
    if app is None:
        logging.error("LangGraph app is not compiled or imported. Cannot run workflow.")
        print("Workflow cannot be run due to errors in graph compilation or imports.")
        return

    logging.info(f"Starting workflow for initial query: '{initial_query}'")

    # Define the initial state for the graph # Ensure the keys match the AgentState TypedDict defined in nodes.py
    initial_state = {
        "new_query": initial_query,
        "reasoning_mode": reasoning_mode_flag,
        "search_queries": [],
        "rationale": None,
        "data": [],
        "relevant_contexts": {},
        "relevant_chunks": [],
        "proceed": True, # Start by proceeding to query generation
        "visited_urls": [],
        "iteration_count": 0,
        "report": None,
        "report_filename": "IntelliSearchReport",
        "error": None,
        "evaluation_response": None,
        "suggested_follow_up_queries": [],
        "prompt_type": prompt_type, # Added prompt type to the state
        "approval_iteration_count": 0,  # Counts loops between user_approval ↔ create_queries
        "search_iteration_count": 0,  # Counts loops from AI_evaluate ↔ evaluate_search_results    
        "report_type": None  # Will be set by choose_report_type node
    }

    # Run the compiled workflow
    try:
        if config is not None:
            astream = app.astream(initial_state, config=config)
        else:
            astream = app.astream(initial_state)

        async for step in astream:
             for key, value in step.items():
                 logging.info("Node executed: %s", key)

        logging.info("Workflow finished.")
        final_report_filename = initial_state.get("report_filename", "No report file generated.")
        logging.info("Check for report files: %s and %s", final_report_filename, (setup.REPORT_FILENAME_PDF if hasattr(setup, 'REPORT_FILENAME_PDF') else 'CrystalSearchReport.pdf')) 

        # Check for any errors in the final state
        final_error_state = initial_state.get('error')
        if final_error_state:
             logging.warning("Workflow completed with errors: %s", final_error_state)


    except Exception as e:
        logging.exception(f"An error occurred during workflow execution: {e}")
        logging.error("An error occurred during workflow execution: %s", e)


# --- Main Execution Block ---
if __name__ == "__main__":
    # Example usage:
    user_research_query = input("Enter your Crystal Research Query: ")

    # Get prompt type from user
    print("\nSelect prompt type:")
    print("1: Legal")
    print("2: General")
    print("3: Macro")
    print("4: DeepSearch")
    print("5: Person Search")
    print("6: Investment Research")
    prompt_type_choice = input("Enter the number for your desired prompt type: ")

    # Map user choice to prompt type string
    prompt_type_mapping = {
        "1": "legal",
        "2": "general",
        "3": "macro",
        "4": "deepsearch",
        "5": "person_search",
        "6": "investment"
    }
    # Get the selected prompt type, default to "general" if input is invalid
    selected_prompt_type = prompt_type_mapping.get(prompt_type_choice, "general")
    print(f"Selected prompt type: {selected_prompt_type}")

    # Get reasoning mode from user
    print("\nSelect reasoning mode:")
    print("1: Reasoning (interpretive, analytical)")
    print("2: Research (factual, coverage-focused)")
    reasoning_mode_choice = input("Enter the number for your desired reasoning mode: ")

    # Map user choice to boolean
    reasoning_mode_flag = True if reasoning_mode_choice == "1" else False
    print(f"Selected reasoning mode: {'Reasoning' if reasoning_mode_flag else 'Research'}")


    # Run the async workflow
    asyncio.run(run_workflow(user_research_query, reasoning_mode_flag, selected_prompt_type))


