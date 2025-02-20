from fastapi import APIRouter, HTTPException, Depends, Response
from app.schemas.users import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlmodel import select
from app.db.sessions import get_session
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Router for authentication
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def get_password_hash(password):
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# POST /auth/register
@router.post("/auth/login")
async def authenticate_user(email: str, password: str, db: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    result = db.execute(statement).first()
    user = result[0] if result else None
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

# POST /auth/logout
@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

