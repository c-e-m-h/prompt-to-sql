from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from db import SessionLocal
from agent import prompt_to_sql

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Anysoft SQL Demo API"}

@app.post("/query")
def query_endpoint(request: QueryRequest):
    # TODO: Add JWT auth here if needed
    sql = prompt_to_sql(request.prompt)
    with SessionLocal() as db:
        result = db.execute(text(sql))
        columns = result.keys()
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
    return {"table": rows, "chart": []}  # TODO: Add chart data logic

