import os
import json
from .llm_service import get_llm_json_response
from ..db.schema_loader import get_database_schema

def load_sql_generation_prompt() -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "sql_generation_prompt.txt")
    with open(prompt_path, "r") as f:
        return f.read()

def generate_sql(user_question: str) -> str | None:
    """
    Passes the clear user question to the LLM to generate a SQL query.
    """
    schema = get_database_schema()
    raw_prompt = load_sql_generation_prompt()
    system_prompt = raw_prompt.format(schema=schema)
    
    try:
        response_text = get_llm_json_response(system_prompt, user_question)
        response_data = json.loads(response_text)
        
        return response_data.get("sql")
    except Exception as e:
        print(f"Error in SQL Generation: {e}")
        return None
