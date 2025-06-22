from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import text
from db import SessionLocal
from agent import prompt_to_sql
from auth import (
    create_access_token, register_user, authenticate_user, get_current_user
)
from models import Query, User

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class QueryRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Anysoft SQL Demo API"}

@app.post("/register")
def register(request: RegisterRequest):
    with SessionLocal() as db:
        user = register_user(db, request.username, request.password)
        return {"message": f"User {user.username} registered successfully."}

@app.post("/login")
def login(request: LoginRequest):
    with SessionLocal() as db:
        user = authenticate_user(db, request.username, request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        user_id = user["id"] if isinstance(user, dict) else user.id
        token = create_access_token(user_id)
        return {"access_token": token, "token_type": "bearer"}

@app.post("/query")
def query_endpoint(request: QueryRequest, user: User = Depends(get_current_user)):
    try:
        sql = prompt_to_sql(request.prompt)
        if sql.strip() == "SELECT 'Please clarify your question.' AS message;":
            raise HTTPException(status_code=400, detail="Unsupported prompt")
    except RuntimeError:
        raise HTTPException(status_code=502, detail="OpenAI API error. Please try again later.")
    with SessionLocal() as db:
        try:
            result = db.execute(text(sql))
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Schema mismatch or invalid SQL: {e}")
        # Save query to DB
        q = Query(user_id=user.id, prompt_text=request.prompt, sql_text=sql, result=rows)
        db.add(q)
        db.commit()
    return {"table": rows, "chart": [], "sql": sql}  # TODO: Add chart data logic

@app.get("/user/queries")
def get_user_queries(user: User = Depends(get_current_user)):
    with SessionLocal() as db:
        queries = (
            db.query(Query)
            .filter(Query.user_id == user.id)
            .order_by(Query.created_at.desc())
            .limit(10)
            .all()
        )
        return [
            {
                "prompt": q.prompt_text,
                "sql": q.sql_text,
                "result": q.result,
                "created_at": q.created_at.isoformat() if q.created_at else None,
            }
            for q in queries
        ]

