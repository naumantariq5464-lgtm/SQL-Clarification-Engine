import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ...schemas.query import QueryRequest, QueryResponse
from ...services.combined_service import process_database_intent
from ...services.sql_validation_service import validate_sql, SQLValidationError
from ...services.query_execution_service import execute_sql_query
from ...services.answer_service import load_answer_prompt
from ...services.llm_service import get_llm_stream_response

router = APIRouter()

@router.post("/query")
async def handle_query(request: QueryRequest):
    async def event_stream():
        # 1. Master LLM Call (Routing + Clarification + SQL)
        response = process_database_intent(request.question, request.history)
        
        if response.intent == "CASUAL":
            yield f"data: {json.dumps({'type': 'metadata', 'needs_clarification': False, 'accuracy_score': 100})}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'content': response.casual_response})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return
            
        if response.needs_clarification:
            yield f"data: {json.dumps({'type': 'metadata', 'needs_clarification': True, 'accuracy_score': response.accuracy_score})}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'content': response.clarification_question})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return
            
        # 3. SQL Validation
        sql_query = response.sql
        if not sql_query:
            yield f"data: {json.dumps({'type': 'error', 'content': 'Failed to generate SQL query.'})}\n\n"
            return
            
        try:
            validate_sql(sql_query)
        except SQLValidationError as e:
            yield f"data: {json.dumps({'type': 'error', 'content': f'Unsafe SQL generated: {e}'})}\n\n"
            return
            
        # Send Metadata
        yield f"data: {json.dumps({'type': 'metadata', 'needs_clarification': False, 'accuracy_score': response.accuracy_score, 'sql': sql_query})}\n\n"
            
        # 4. Query Execution
        db_result = execute_sql_query(sql_query)
        if db_result is None:
            yield f"data: {json.dumps({'type': 'error', 'content': 'Failed to execute SQL query.'})}\n\n"
            return
            
        # 5. Answer Formatting (Streaming)
        system_prompt = load_answer_prompt().replace("{question}", request.question).replace("{db_result}", json.dumps(db_result, default=str))
        
        for chunk in get_llm_stream_response(system_prompt, request.question):
            yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
            
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        
    return StreamingResponse(event_stream(), media_type="text/event-stream")
