from fastapi import FastAPI, APIRouter, HTTPException, Depends
from app.schemas.users import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlmodel import select
from app.db.sessions import get_session

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/admin/users")
async def register_user(name: str, email: str, password: str, role: str, db: Session = Depends(get_session)):
    # Check if user already exists
    statement = select(User).where(User.email == email)
    existing_user = db.execute(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = get_password_hash(password)

    # Create a new user
    new_user = User(name=name, email=email, password=hashed_password, role=role, activation=False)
    
    # Add user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user": new_user}