import os
import json
from ..services.llm_service import get_llm_json_response
from ..db.schema_loader import get_database_schema
from ..schemas.query import QueryResponse

def load_clarification_prompt() -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "clarification_prompt.txt")
    with open(prompt_path, "r") as f:
        return f.read()

def process_query_for_clarification(user_question: str) -> QueryResponse:
    """
    Passes the user's question to the LLM to determine if it is ambiguous.
    """
    schema = get_database_schema()
    raw_prompt = load_clarification_prompt()
    system_prompt = raw_prompt.format(schema=schema)
    
    try:
        response_text = get_llm_json_response(system_prompt, user_question)
        response_data = json.loads(response_text)
        
        return QueryResponse(
            needs_clarification=response_data.get("needs_clarification", False),
            clarification_question=response_data.get("clarification_question"),
            accuracy_score=response_data.get("confidence_score")
        )
    except Exception as e:
        # In a real app, use a logger.
        print(f"Error in Clarification Engine: {e}")
        return QueryResponse(
            needs_clarification=True,
            clarification_question="Sorry, I encountered an error processing your query. Could you rephrase it?"
        )
