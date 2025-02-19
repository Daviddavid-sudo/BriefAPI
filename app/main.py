from fastapi import FastAPI
from app.endpoints.loans import router as loan_router
# from app.endpoints.users import router as user_router

from app.endpoints import authentification

app = FastAPI()

# Inclure les routes de 'loan_router'
app.include_router(loan_router)
# app.include_router(user_router)
app.include_router(authentification.router)
