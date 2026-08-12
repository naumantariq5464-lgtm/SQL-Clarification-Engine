from sqlalchemy import text
from ..db.database import SessionLocal

def execute_sql_query(sql_query: str) -> list[dict] | None:
    """
    Executes a validated read-only SQL query against the Neon PostgreSQL database
    and returns the result as a list of dictionaries.
    """
    db = SessionLocal()
    try:
        # Wrap query in text() for SQLAlchemy
        result = db.execute(text(sql_query))
        
        # Convert result rows into a list of dicts
        # Using dict(row._mapping) is the modern SQLAlchemy way to convert rows to dict
        rows = [dict(row._mapping) for row in result]
        return rows
        
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        db.close()
