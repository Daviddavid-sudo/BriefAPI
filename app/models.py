from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy.ext.declarative import declarative_base

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    role: str
    activation: bool = Field(default=False)


class loan_requests(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    state: str
    bank: str
    term: int
    naics: int
    newexist: bool
    year: int
    createjob: int
    franchisecode: int
    revline: int
    lowdoc: int
    grappv: int
    sbaappv: int
    urbanrural: int
    accepted: bool 