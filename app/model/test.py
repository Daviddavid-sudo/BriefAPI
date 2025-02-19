import pandas as pd
from app.models import LoanRequest
from app.database import Session, engine

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv('chemin/vers/ton/fichier.csv')

# Affiche les premières lignes pour vérifier
print(df.head())

# Ouvrir une session de base de données
with Session(engine) as session:
    # Itérer sur chaque ligne du DataFrame et ajouter les données à la base
    for index, row in df.iterrows():
        loan_request = LoanRequest(
            user_id=row['user_id'],  # Adapte les noms de colonnes selon ton CSV
            loan_amount=row['loan_amount'],
            interest_rate=row['interest_rate'],
            duration=row['duration'],
            # Ajoute d'autres colonnes si nécessaire
        )
        session.add(loan_request)

    # Committer les modifications dans la base de données
    session.commit()

    print("Données insérées avec succès!")
