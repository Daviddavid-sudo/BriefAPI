from sqlmodel import SQLModel, Field, create_engine, Session
# from models import User, loan_requests

sqlite_url = "sqlite:///db.sqlite"
engine = create_engine(sqlite_url, echo=True)
session = Session(bind=engine)  

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():  
    create_db_and_tables()   


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":  
    main()
    get_session()
