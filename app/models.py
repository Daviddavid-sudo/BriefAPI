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
    State: str
    NAICS: int
    UrbanRural: int
    LowDoc: str 
    bank_loan_float: float
    SBA_loan_float: float
    FranchiseCode: str
    Bank: str
    BankState: str
    RevLineCr: str 
    Term: int
    crisis: int