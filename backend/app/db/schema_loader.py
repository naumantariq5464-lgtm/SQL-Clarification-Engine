from sqlalchemy import inspect
from .database import engine
from .models import Base

def get_database_schema() -> str:
    """
    Reads the SQLAlchemy models and generates a text representation of the database schema
    to be injected into the LLM prompts.
    """
    inspector = inspect(engine)
    schema_details = []
    
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        col_details = []
        for col in columns:
            col_info = f"{col['name']} ({col['type']})"
            col_details.append(col_info)
            
        schema_details.append(f"Table: {table_name}")
        schema_details.append(f"Columns: {', '.join(col_details)}")
        schema_details.append("-" * 20)
        
    return "\n".join(schema_details)
