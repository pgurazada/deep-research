import os
import dspy
import uvicorn
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Deep Research API",
    description="An API serving a DSPy program that conducts deep research using web search",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQlite for logging

def init_db():
    conn = sqlite3.connect('backend/research-logs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            query TEXT NOT NULL,
            result TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(query, result):
    conn = sqlite3.connect('backend/research-logs.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO research_logs (query, result) VALUES (?, ?)', (query, result))
    conn.commit()
    conn.close()

init_db()

# --- Load and serve the optimized sentiment analyzer ---

lm = dspy.LM(
    model='openai/gpt-4o-mini',
    temperature=0,
    api_key=os.environ['OPENAI_API_KEY']
)

dspy.settings.configure(lm=lm, async_max_workers=8)

web_search_agent = dspy.load('backend/output/deep-research-agent')
web_search_agent_async = dspy.asyncify(web_search_agent)

class Query(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Deep Research API!"}

@app.post("/answer")
async def answer(query: Query):
    try:
        result = await web_search_agent_async(query.text)
        log_interaction(query.text, result)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, workers=4)