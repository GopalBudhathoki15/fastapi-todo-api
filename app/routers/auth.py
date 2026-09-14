from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.schemas import UserResponse, UserCreate, UserLogin, LoginResponse
from app.models import User
from app.security import hash_password, verify_password, SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime, timezone, timedelta

if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY is not set")


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.scalars(select(User).where(User.email == user.email)).one_or_none()

    if db_user:
        raise HTTPException(status_code=409, detail="User already exists.")

    hashed_password = hash_password(user.password)

    new_user = User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", status_code=200, response_model=LoginResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    db_user = db.scalars(
        select(User).where(User.email == credentials.email)
    ).one_or_none()

    if db_user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    is_verified = verify_password(credentials.password, db_user.hashed_password)

    if not is_verified:
        raise HTTPException(status_code=401, detail="Authentication failed")

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=30)

    token = jwt.encode(
        {"sub": str(db_user.id), "exp": expires_at},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return LoginResponse(access_token=token, token_type="bearer")
