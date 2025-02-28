from app.db.sessions import get_session
from app.schemas.users import User
import bcrypt

def hash_password(password: str) -> str:
    """Hash the password for storage."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def add_multiple_users():
    users_data = [
        {"name": "Dorothée", "email": "dorothee@example.com", "password": "dorotheepass", "role": "admin"},
        {"name": "David", "email": "david@example.com", "password": "davidpass", "role": "user"},
        {"name": "Sami", "email": "sami@example.com", "password": "samipass", "role": "user"},
    ]

    
    session = next(get_session())  # Récupération d'une session unique
    try:
        for user_data in users_data:
            hashed_password = hash_password(user_data['password'])
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=hashed_password,
                role=user_data['role'],
                is_active=True  # On active les comptes par défaut
            )

            session.add(user)

        session.commit()
        print("Multiple users have been added successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

add_multiple_users()