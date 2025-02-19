from fastapi import FastAPI
from app.endpoints import authentification

app = FastAPI()

app.include_router(authentification.router)
