from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import query

app = FastAPI(
    title="Text-to-SQL Clarification Engine API",
    description="API for converting natural language to SQL with ambiguity detection.",
    version="1.0.0"
)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Text-to-SQL API is running."}
