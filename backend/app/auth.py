import jwt, datetime, os, logging
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from models import User
from db import SessionLocal  # Import here to avoid circular import

SECRET = os.getenv("JWT_SECRET", "dev-secret")

security = HTTPBearer()

# Hardcoded demo user
DEMO_USER = "demo"
DEMO_PASS = "demopass"
DEMO_ID = -1
DEMO_HASH = bcrypt.hash(DEMO_PASS)

def create_access_token(user_id: int):
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = verify_token(credentials.credentials)
    logging.info(f"User ID from token: {user_id}")
    if user_id == DEMO_ID:
        logging.info("Demo user authenticated.")
        return user_id
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logging.warning(f"User ID {user_id} not found in DB.")
            raise HTTPException(status_code=401, detail="User not found")
        logging.info(f"User ID {user_id} found in DB.")
        return user

# Registration logic
def register_user(db: Session, username: str, password: str):
    if username == DEMO_USER:
        raise HTTPException(status_code=400, detail="Username not allowed.")
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists.")
    hashed = bcrypt.hash(password)
    new_user = User(username=username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login logic
def authenticate_user(db: Session, username: str, password: str):
    if username == DEMO_USER and bcrypt.verify(password, DEMO_HASH):
        return {"id": DEMO_ID, "username": DEMO_USER}
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        return None
    return user 