# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from app.migrations.env import SECRET_KEY, ALGORITHM  # Importer les variables depuis env.py

# def create_access_token(data: dict):

#     expires_delta = timedelta(hours=1)
#     expiration = datetime.utcnow() + expires_delta

#     # Créer le payload (données à inclure dans le token)
#     to_encode = data.copy()
#     to_encode.update({"exp": expiration})

#     # Créer le token JWT
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt



# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expiration = datetime.utcnow() + timedelta(hours=1)  # Durée de validité du token (1 heure ici)
#     to_encode.update({"exp": expiration})  # Ajoute la date d'expiration au payload
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Crée le token signé
#     return encoded_jwt