from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlmodel import Session, select, SQLModel
from init_db import engine  
from models import User
from crud import create_user
import bcrypt 
# import jwt

app = FastAPI()



#creation user
class UserCreate(BaseModel):
    email: str
    password: str
    name : str
    id : int

@app.post("/users")
def create_user(user: UserCreate):
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
@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()

        return [{"Nom de l'utilisateur" : user.name} for user in users]









































# class LoginRequest(BaseModel):
#     email: str
#     password: str

# @app.post("/login")
# def login(user: LoginRequest):
#     with Session(engine) as session:
#         db_user = session.exec(select(User).where(User.email == user.email)).first()
#         if db_user is None:
#             return "Utilisateur non trouvé"
        
#         if db_user.password != user.password:
#             return "Mot de passe incorrect"

#         return "Connexion réussie"