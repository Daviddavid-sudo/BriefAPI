from sqlmodel import SQLModel, create_engine
from app.schemas.users import User
from app.schemas.loans import LoanRequest

# Unique definition of the URL and engine
DATABASE_URL = "sqlite:///app/db/loans.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Creates the database tables if they do not exist."""
    SQLModel.metadata.create_all(engine)
    print("✔️  Database and tables created.")

if __name__ == "__main__":  
    create_db_and_tables()
