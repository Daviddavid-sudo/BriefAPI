from fastapi import FastAPI, Depends, HTTPException, Header, APIRouter
from pydantic import BaseModel
from sqlmodel import Session, select, SQLModel
from app.database import engine  
from app.models import User
import bcrypt 
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import datetime
router = APIRouter()


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/users")
def create_user(user: User):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            return {"Un utilisateur avec cet email existe déjà"}
        
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(email=user.email, password=hashed_password.decode('utf-8'), name=user.name, role=user.role, activation=False)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return "Inscription validée"




#verification admin ou non
def verify_admin(token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token manquant")
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit")
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Token expiré")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Token invalide")
    
    return payload  

#liste user
@router.get("/users")
def get_users():
    if verify_admin(Depends(oauth2_scheme)):
        with Session(engine) as session:
            users = session.exec(select(User)).all()

            return [{"Nom de l'utilisateur" : user.name} for user in users]
