from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.users import User


# Fonction pour obtenir l'heure actuelle en UTC
def get_current_time():
    return datetime.now(timezone.utc)

# Define the LoanRequest model
class LoanRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, )
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="loans")
    # Loan request status
    accepted : Optional[bool] = Field(default=False)
    
    # Loan request attributes
    Amount: float           # The loan amount
    Term: float               # The loan term
    LowDoc: str             # LowDoc = Y, Not LowDoc = N
    RevLineCr: str          # RevLineCr = 1, Not RevLineCr = 0
    
    NoEmp: float              # Number of employees
    
    NAICS: str              # North American Industry Classification System
    New: str                # New = 1, Existing = 0
    Franchise: str          # Franchise = 1, Non-Franchise = 0

    # Loan request location attributes
    State: str              # State abbreviation
    Rural: str              # Urban = 0, Rural = 1, Undefined = None



        
