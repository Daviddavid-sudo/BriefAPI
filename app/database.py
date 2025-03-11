import os
import pyodbc
from sqlmodel import SQLModel, Field, create_engine, Session
from app.models import User, loan_requests

# Constants
SERVER = 'skabdanisqlserver.database.windows.net'
USERNAME = 'skabdaniadmin'
PASSWORD = os.getenv("DB_PASSWORD")  # Ensure this environment variable is set correctly
DRIVER = '{ODBC Driver 18 for SQL Server}'
DATABASE = 'skabdani_ussba'

# Connection URL for SQLAlchemy
DATABASE_URL = f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server"

# Create the engine at the module level so it can be imported
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

def get_connection():
    """Establish a connection to the SQL Server using pyodbc."""
    try:
        conn = pyodbc.connect(
            f'DRIVER={DRIVER};SERVER={SERVER};PORT=1433;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        )
        return conn
    except pyodbc.InterfaceError as e:
        print(f"Error connecting to the database: {e}")
        return None

def test_connection():
    """Test the connection to the database with a simple query."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Simple query to check connection
        row = cursor.fetchone()
        if row:
            print("Connection successful!")
        else:
            print("Connection failed: No data returned.")
        conn.close()
    else:
        print("Failed to connect to the database.")

def create_db_and_tables():
    """Create the database tables if they don't exist."""
    SQLModel.metadata.create_all(engine, checkfirst=True)

def get_session():
    """Return a session to interact with the database."""
    with Session(engine) as session:
        yield session

def main():
    """Main function to set up the database and tables."""
    create_db_and_tables()
    test_connection()  # Test the connection after setup

if __name__ == "__main__":
    main()


# from sqlmodel import SQLModel, Field, create_engine, Session
# from app.models import User, loan_requests
# import pyodbc
# import os

# server = 'skabdanisqlserver.database.windows.net'
# username = 'skabdaniadmin'
# password = os.getenv("DB_PASSWORD")  
# driver = '{ODBC Driver 18 for SQL Server}'
# database = 'skabdani_ussba'
# print(f"drivers : {pyodbc.drivers()}")

# DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+18+for+SQL+Server"

# conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database}; PORT=1433; UID={username};PWD={password}')

# cursor = conn.cursor()
# cursor.execute("SELECT 1")  # Simple requête pour tester la connexion
# row = cursor.fetchone()
# if row:
#     print("Connexion réussie !")
# else:
#     print("Erreur de connexion.")

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# session = Session(bind=engine)  

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine, checkfirst=True)

# def main():  
#     create_db_and_tables()   

# def get_session():
#     with Session(engine) as session:
#         yield session

# main()