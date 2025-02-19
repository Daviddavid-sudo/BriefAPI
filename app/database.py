from sqlmodel import SQLModel, Field, create_engine, Session
from app.models import User, loan_requests

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():  
    create_db_and_tables()   

# user = User
# loan_requests = loan_requests

if __name__ == "__main__":  
    main()

def get_session():
    with Session(engine) as session:
        yield session