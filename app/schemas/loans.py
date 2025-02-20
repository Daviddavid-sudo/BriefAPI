from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime, timezone
from app.schemas.users import User


def get_current_time():
    return datetime.now(timezone.utc)

# Define the LoanRequest model
class LoanRequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="loans")
    created_at: datetime = Field(default_factory=datetime.now)

    # General Business Information
    naics: str
    new_business: bool
    year: str

    # Location
    state: str
    urbanrural: int

    # Bank
    bank: str
    bankstate: str
    franchisecode: str

    # Loan Amounts and Conditions
    amount: int
    term: int
    sba_guaranteed: int
    lowdoc: int
    revline: int

    # Economic Impact
    createjob: int

    # Loan Status
    status: bool

    # Default value for crisis
    crisis: int = Field(default=0)  # Par défaut, crisis est 0

    def to_features(self) -> List[List]:
        """
        Convert the loan request data into a structured list of features for prediction.
        """
        return [[
            self.naics, self.new_business, self.state, self.urbanrural,
            self.bank, self.bankstate, self.franchisecode, self.amount, self.term,
            self.sba_guaranteed, self.lowdoc, self.revline, self.createjob, self.crisis
        ]]



        
