from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Form

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str

class LoanRequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    state: str
    bank: str
    term: int
    naics: str
    newexist: bool #(0/1)
    year: str
    createjob: int
    franchisecode: int
    revline: int
    lowdoc: int
    grappv: int
    sbaappv: int
    urbanrural: int
    accepted: bool

