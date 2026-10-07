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

## Setup Instructions

### 1. Environment Variables
You need to create a `.env` file in the root directory. This file should contain your database connection string and your Groq API key. **Do not commit your `.env` file or share your actual keys.**

Create a file named `.env` and add the following keys:

```ini
# PostgreSQL connection string (Example format)
DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require

# Groq API Key for LLM
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Backend Setup
Navigate to the `backend` folder, create a virtual environment, install the dependencies, and start the FastAPI server.

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Start the backend server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 3. Frontend Setup
Open a new terminal window, navigate to the `frontend` folder, install packages, and run the Next.js development server.

```bash
cd frontend
npm install

# Start the frontend server
npm run dev
```

### 4. Open the App
Once both servers are running, open your browser and navigate to:
👉 **http://localhost:3000**
