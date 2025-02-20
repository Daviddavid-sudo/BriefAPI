from sqlmodel import SQLModel, Field, Relationship
from typing import List

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    role: str
    loans: List["LoanRequest"] = Relationship(back_populates="user")
