import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

client = Groq(api_key=GROQ_API_KEY)
DEFAULT_MODEL = "openai/gpt-oss-20b"

def get_llm_json_response(system_prompt: str, user_prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Sends a prompt to the Groq API and expects a JSON formatted response.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=model,
            response_format={"type": "json_object"},
            temperature=0.0
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "{}"

def get_llm_stream_response(system_prompt: str, user_prompt: str):
    """
    Calls the Groq API and returns a generator that yields text chunks.
    """
    try:
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            model=DEFAULT_MODEL,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        print(f"Error streaming from Groq API: {e}")
        yield "An error occurred while generating the response."
