import os
import json
from .llm_service import get_llm_json_response

def load_answer_prompt() -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "answer_prompt.txt")
    with open(prompt_path, "r") as f:
        return f.read()

def generate_natural_answer(user_question: str, db_result: list[dict]) -> str:
    """
    Passes the database result back to the LLM to format it into a conversational answer.
    """
    if not db_result:
        return "I couldn't find any data matching your request."
        
    # Convert result to string for the prompt
    db_result_str = json.dumps(db_result, default=str)
    
    raw_prompt = load_answer_prompt()
    system_prompt = raw_prompt.format(question=user_question, db_result=db_result_str)
    
    try:
        response_text = get_llm_json_response(system_prompt, user_question)
        response_data = json.loads(response_text)
        
        return response_data.get("answer", "Here are the results."), response_data.get("confidence_score", 100)
    except Exception as e:
        print(f"Error in Answer Generation: {e}")
        return "I found the results, but I encountered an error formatting them.", 0
