from models import User
from sqlmodel import Field, Session, SQLModel, create_engine


sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=True)

def create_user():
    user_1 = User(id=1802, name="sami", email="sami@gmail.com", password="samisami")
    with Session(engine) as session:
        session.add(user_1)
        session.commit()


if __name__ == "__main__":
    create_user()
