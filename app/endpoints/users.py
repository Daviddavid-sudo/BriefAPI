from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header
from app.models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlmodel import select
from app.database import *
from app.database import get_session
import bcrypt 
import jwt

router = APIRouter()
# JWT Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# @router.post("/admin/users")
# async def register_user(name: str, email: str, password: str, role: str, db: Session = Depends(get_session)):
#     # Check if user already exists
#     statement = select(User).where(User.email == email)
#     existing_user = db.execute(statement).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Hash the password
#     hashed_password = get_password_hash(password)

#     # Create a new user
#     new_user = User(name=name, email=email, password=hashed_password, role=role, activation=False)
    
#     # Add user to database
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     return {"message": "User registered successfully", "user": new_user}

@router.post("/users")
def create_user(user: User):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            return {"Un utilisateur avec cet email existe déjà"}
        
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(email=user.email, password=hashed_password.decode('utf-8'), name=user.name, id=user.id)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return "Inscription validée"

        # return {"id": new_user.id, "email": new_user.email, "name" : new_user.name, "password" : new_user.password }



#verification admin ou non
def verify_admin(token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token manquant")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Accès interdit")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")
    
    return payload  


#liste user
@router.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()

        return [{"Nom de l'utilisateur" : user.name} for user in users]





