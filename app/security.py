from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
import jwt
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import User
from app.database import get_db
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY is not set")
password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
        db_user = db.scalars(select(User).where(User.id == user_id)).one_or_none()

        if db_user is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )

        return db_user
    except (jwt.InvalidTokenError, ValueError, KeyError):
        raise HTTPException(status_code=401, detail="Could not validate credentials")
