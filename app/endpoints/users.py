from fastapi import FastAPI, Depends, HTTPException, Header, APIRouter, status
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlmodel import Session, select, SQLModel
from app.database import engine, get_session
from app.models import User
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/users")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        statement = select(User).where(User.email == email)
        result = db.execute(statement).first()
        user = result[0] if result else None

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
    except JWTError as e:
        print("JWT Error:", str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


@router.post("/admin/users")
def create_user(user: User):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            return {"Un utilisateur avec cet email existe déjà"}
        
        hashed_password = jwt.encode(user.password)

        new_user = User(email=user.email, password=hashed_password, name=user.name, role=user.role, activation=False)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return "Inscription validée"


    
@router.get("/admin/users")
def get_users(current_user: User = Depends(get_current_user)):
    # Ensure current_user is valid
    if not current_user or not hasattr(current_user, "role"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user authentication")

    # Check if the user is an admin
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    # Fetch all users from the database
    with Session(engine) as session:
        users = session.execute(select(User)).all()
        #return [{"Nom de l'utilisateur": user.name} for user in users]
        return {
            "Liste des utilisateurs" : [user[0].name for user in users]
        }

