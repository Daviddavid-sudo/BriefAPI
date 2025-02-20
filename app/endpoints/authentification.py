from fastapi import FastAPI, APIRouter, HTTPException, Depends, Response
from app.models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from sqlmodel import select
from app.database import get_session
from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# JWT Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/auth/login")
async def authenticate_user(email: str, password: str, db: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    result = db.execute(statement).first()
    user = result[0] if result else None
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

    # return user


@router.post("/auth/logout")
def logout(response : Response):
  response = RedirectResponse('/auth/login', status_code= 302)
  response.delete_cookie(key ='access_token')
  return response