from models import *

def add_user(name: str, email: str):
    with Session(engine) as session:
        user = User(name=name)
        session.add(user)
        session.commit()

add_user("david", "david")