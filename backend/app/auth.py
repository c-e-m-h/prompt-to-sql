import jwt, datetime, os
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.hash import bcrypt

SECRET = os.getenv("JWT_SECRET", "dev-secret")

security = HTTPBearer()

def create_access_token(user_id: int):
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
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
    return verify_token(credentials.credentials) 