from sqlmodel import SQLModel, Field, Relationship
from typing import List

class User(SQLModel, table=True):
    """
    User model representing a user in the system.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        password_hash (str): Hashed password for the user.
        role (str): Role of the user (e.g., admin, user).
        is_active (bool): Indicates if the user has activated their account. Defaults to False.
        loans (List["LoanRequest"]): Relationship to the LoanRequest model, representing the loans associated with the user.
    """
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    role: str
    is_active: bool = False  # Champ indiquant si l'utilisateur a activé son compte
    loans: List["LoanRequest"] = Relationship(back_populates="user")
    
    
    