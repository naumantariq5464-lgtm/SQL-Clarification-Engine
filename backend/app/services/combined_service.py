import os
import json
from ..services.llm_service import get_llm_json_response
from ..db.schema_loader import get_database_schema
from ..schemas.query import QueryResponse, ChatMessage
from typing import List, Tuple

def load_combined_prompt() -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "combined_sql_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def process_database_intent(question: str, history: List[ChatMessage]) -> QueryResponse:
    schema = get_database_schema()
    base_prompt = load_combined_prompt()
    
    # Format history
    history_str = ""
    for msg in history:
        history_str += f"{msg.role.capitalize()}: {msg.content}\n"
        
    if not history_str:
        history_str = "No previous history."
        
    system_prompt = base_prompt.replace("{schema}", schema).replace("{history}", history_str).replace("{question}", question)
    
    try:
        response_text = get_llm_json_response(system_prompt, question)
        response_data = json.loads(response_text)
        
        return QueryResponse(
            intent=response_data.get("intent", "DATABASE"),
            casual_response=response_data.get("casual_response"),
            needs_clarification=response_data.get("needs_clarification", False),
            clarification_question=response_data.get("clarification_question"),
            sql=response_data.get("sql"),
            accuracy_score=response_data.get("confidence_score")
        )
    except Exception as e:
        print(f"Error in Combined Service: {e}")
        return QueryResponse(
            needs_clarification=True,
            clarification_question="I encountered an error understanding your request. Could you rephrase it?",
            accuracy_score=0
        )
