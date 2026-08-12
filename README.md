# SQL Clarification Engine

> **IMPORTANT NOTE:** This project is currently under active development.

The SQL Clarification Engine is an AI-powered database assistant that translates natural language questions into PostgreSQL queries. 

## Features
- **Intelligent Routing**: Determines if a user's intent is casual conversation or a database query.
- **Auto-Clarification**: Detects ambiguous questions (e.g. "who is our best customer?") and automatically asks the user for clarification before executing potentially wrong SQL.
- **Real-Time Streaming (SSE)**: Streams AI responses token-by-token directly to the frontend for a fast, ChatGPT-like experience.
- **Blazing Fast Latency**: Uses advanced prompt engineering to combine Routing, Clarification, and SQL generation into a single LLM call, plus SQLAlchemy Connection Pooling for zero database connection overhead.

## Tech Stack
- **Frontend**: Next.js, React, TailwindCSS, Framer Motion
- **Backend**: FastAPI, SQLAlchemy, Python
- **AI Model**: Llama 3 (via Groq API)
- **Database**: PostgreSQL (Neon)
