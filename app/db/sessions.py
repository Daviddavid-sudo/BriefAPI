from sqlmodel import Session
from app.db.database import engine
from typing import Generator

def get_session() -> Generator[Session, None, None]:
    """
    Provides a database session to FastAPI for a given request.

    Yields:
        Generator[Session, None, None]: A SQLAlchemy session object.
    """
    """Fournir une session à FastAPI pour une requête donnée."""
    with Session(engine) as session:
        yield session

