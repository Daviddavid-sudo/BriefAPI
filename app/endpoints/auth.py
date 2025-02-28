from fastapi import FastAPI, APIRouter, HTTPException, Depends, Response, status, Header
from app.models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from app.database import get_session, engine
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import timedelta, datetime


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta  # Use `utcnow()` for consistency
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


        # Fetch user from the database
        statement = select(User).where(User.email == email)
        result = db.execute(statement).first()
        user = result[0] if result else None

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


class ResetPasswordRequest(BaseModel):
    new_password: str
    confirm_password: str


@router.post("/auth/login")
async def authenticate_user(email: str, password: str, db: Session = Depends(get_session)):
    statement = select(User).where(User.email == email)
    result = db.execute(statement).first()
    user = result[0] if result else None
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):

    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match."
        )

    hashed_password = get_password_hash(request.new_password)
    current_user.password = hashed_password
    current_user.activation = True 

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"success": True, "message": "Password reset successful, account activated!"}


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}



