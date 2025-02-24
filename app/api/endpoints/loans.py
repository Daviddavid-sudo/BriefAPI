from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.schemas.loans import LoanRequest
from app.schemas.users import User
#from auth import get_current_user

from app.db.sessions import get_session
import joblib
import numpy as np
import lightgbm
import pandas as pd
import joblib

router = APIRouter()

### Routes for loan requests ###
# Load the pre-trained model for loan eligibility prediction
model = joblib.load("app/models/final_model_pipeline.pkl")


# GET /loans/request
@router.post("/loans/request", response_model=LoanRequest)
async def request_loan_and_predict(loan_request: LoanRequest):
    """
    Submits a loan request and predicts the eligibility based on the request.

    Args:
        user_id (int): The ID of the user submitting the loan request.
        loan_request (LoanRequest): The loan request data.
        session (Session): SQLAlchemy database session.

    Returns:
        dict: A message with the eligibility status and the updated loan request.
    """
    # Retrieve the user from the database using the provided user_id
    #user = session.get(User, user_id)
    #if not user:
    #    raise HTTPException(status_code=404, detail="User not found")

    # Create a new loan request instance
    new_loan_request = LoanRequest(**loan_request.model_dump(exclude_unset=True))

    #try:
        # Add the new loan request to the session
    #session.add(new_loan_request)
        # Commit the transaction to save the new loan request in the database
    #session.commit()
        # Refresh the session to get the updated loan request data
    #session.refresh(new_loan_request)
    #except Exception as e:
        # If an exception occurs during the database transaction, rollback the session and raise an error
    #session.rollback()
        #raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # Map LoanRequest attributes to model features for prediction
    loan_data = {
        "GrAppv": [new_loan_request.Amount],
        "Term": [new_loan_request.Term],
        "LowDoc": [new_loan_request.LowDoc],
        "RevLineCr": [new_loan_request.RevLineCr],
        "NoEmp": [new_loan_request.NoEmp],
        "NAICS_Sectors": [new_loan_request.NAICS],
        "New": [new_loan_request.New],
        "Franchise": [new_loan_request.Franchise],
        "State": [new_loan_request.State],
        "Rural": [new_loan_request.Rural]
    }

    


    # Ensure correct feature transformations
    df_data = pd.DataFrame(loan_data)
    categorical_columns = ['State', 'NAICS_Sectors', 'Franchise', 'Rural', 'LowDoc', 'RevLineCr', 'NoEmp', 'New']
    numeric_columns = ['GrAppv', 'Term']

    # Convert the loan data to a DataFrame
    df_data[categorical_columns] = df_data[categorical_columns].astype('category')
    df_data[numeric_columns] = df_data[numeric_columns].astype('float')
    
    # Vérifiez les colonnes attendues par le modèle
    print(model.feature_names_in_)  # Si disponible, affiche les colonnes attendues par le modèle
    print(df_data.columns)          # Comparez avec les colonnes de df_data

    # Make a prediction using the trained LGBM model
    prediction = model.predict(df_data)

    # Update the 'accepted' column in the loan request if eligible
    new_loan_request.accepted = True if prediction[0] == 1 else False

    # Commit the updated loan request to the database
    #try:
    #loan_request = LoanRequest(**loan_data)
    #loan_request = LoanRequest(**loan_data.dict(exclude={"id", "user_id"}),  # Exclure id et user_id des données envoyées
    #                            user_id=current_user.id)  # Ajouter l'ID de l'utilisateur connecté
    #session.commit()
    #session.refresh(new_loan_request)  # Ensure we have the latest data
#except Exception as e:
    #session.rollback()
        #raise HTTPException(status_code=500, detail=f"Database error while updating eligibility: {str(e)}")

    # Prepare the eligibility message
    eligibility_message = "Your loan request has been accepted." if new_loan_request.accepted else "Your loan request has not been accepted."

    # Return a message with the eligibility status and the updated loan request
    return {
        "message": eligibility_message,
        "loan_request": new_loan_request
    }


# History of loan requests
# GET /loans/history
@router.get("/loans/history")
async def get_loan_history(user_id: int, session: Session = Depends(get_session)):
    # Execute a SQL query to select all loan requests for the given user_id
    loans = session.exec(select(LoanRequest).where(LoanRequest.user_id == user_id)).all()
    # If no loan requests are found, raise a 404 HTTP exception
    if not loans:
        raise HTTPException(status_code=404, detail="No loan requests found")
    # Return the list of loan requests
    return loans

