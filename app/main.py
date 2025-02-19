from fastapi import FastAPI
from app.endpoints.loans import router as loan_router
from app.endpoints import authentification
from app.endpoints import users

app = FastAPI()

# Inclure les routes de 'loan_router'
app.include_router(loan_router)
# app.include_router(user_router)
app.include_router(authentification.router)
app.include_router(users.router)
