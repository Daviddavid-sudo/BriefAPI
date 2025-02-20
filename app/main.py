from fastapi import FastAPI
from app.api.endpoints.loans import router as loan_router
from app.api.endpoints.users import router as user_router
from app.api.endpoints.auth import router as auth_router

app = FastAPI()

# Inclure les routes de 'loan_router'
app.include_router(loan_router)
app.include_router(user_router)
app.include_router(auth_router)

