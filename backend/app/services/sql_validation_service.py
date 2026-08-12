import re

class SQLValidationError(Exception):
    pass

def validate_sql(sql_query: str) -> bool:
    """
    Ensures the generated SQL query is a read-only SELECT statement 
    and does not contain dangerous operations.
    """
    if not sql_query:
        raise SQLValidationError("SQL query is empty.")

    # Convert to uppercase for easier matching
    query_upper = sql_query.upper().strip()

    # Must start with SELECT
    if not query_upper.startswith("SELECT"):
        raise SQLValidationError("Only SELECT queries are allowed.")

    # Block dangerous keywords anywhere in the query
    dangerous_keywords = [
        "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", 
        "TRUNCATE", "GRANT", "REVOKE", "COMMIT", "ROLLBACK", "EXEC"
    ]
    
    # We use regex word boundaries to avoid matching substrings 
    # e.g., an email address containing "update"
    for keyword in dangerous_keywords:
        if re.search(rf'\b{keyword}\b', query_upper):
            raise SQLValidationError(f"Dangerous keyword '{keyword}' detected in query.")

    return True
