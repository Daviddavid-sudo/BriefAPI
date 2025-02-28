from fastapi import FastAPI
from app.endpoints import loans
from app.endpoints import auth
from app.endpoints import users

app = FastAPI()

# Inclure les routes de 'loan_router'
app.include_router(loans.router)
# app.include_router(user_router)
app.include_router(auth.router)
app.include_router(users.router)
