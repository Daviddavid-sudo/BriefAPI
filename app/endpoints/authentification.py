from fastapi import FastAPI, APIRouter, HTTPException, Depends, Response
from app.models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from sqlmodel import select
from app.database import get_session

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/auth/login")
async def authenticate_user(email: str, password: str, db: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    result = db.execute(statement).first()
    user = result[0] if result else None
    print(email,password)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return user


@router.post("/auth/logout")
def logout(response : Response):
  response = RedirectResponse('/auth/login', status_code= 302)
  response.delete_cookie(key ='access_token')
  return response