from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.schemas.loans import LoanRequest
from app.schemas.users import User
from app.db.sessions import get_session
import joblib
import numpy as np
import lightgbm as lgb
import pandas as pd

router = APIRouter()

### Routes for loan requests ###
# Load the pre-trained model for loan eligibility prediction
model = joblib.load("app/models/lgbm_model.pkl")  # Ensure the model file is present in the correct path

# GET /loans/predict
@router.get("/loans/predict")
async def predict_loan_eligibility(loan_id: int, session: Session = Depends(get_session)):
    """
    Predicts loan eligibility based on a loan request ID.

    Args:
        loan_id (int): The ID of the loan request.
        session (Session): SQLAlchemy database session.

    Returns:
        dict: Prediction result indicating whether the loan is eligible or not.
    """
    try:
        # 1Retrieve the loan request from the database
        loan_request = session.get(LoanRequest, loan_id)


        # Handle the case where the loan ID does not exist
        if not loan_request:
            raise HTTPException(status_code=404, detail="Loan request not found")

        # Map LoanRequest attributes to model features
        loan_data = {
            "State": loan_request.state,
            "NAICS": loan_request.naics,
            "UrbanRural": loan_request.urbanrural,
            "LowDoc": loan_request.lowdoc,
            "FranchiseCode": loan_request.franchisecode,
            "Bank": loan_request.bank,
            "BankState": loan_request.bankstate,
            "RevLineCr": loan_request.revline,
            "Term": loan_request.term,
            "bank_loan_float": float(loan_request.amount),  # Convert GrAppv to float
            "SBA_loan_float": float(loan_request.sba_guaranteed),  # Convert SBA_Appv to float
            "crisis": loan_request.crisis,
        }

        # Define the expected feature order
        feature_order = [
            "State", "NAICS", "UrbanRural", "LowDoc", "bank_loan_float",
            "SBA_loan_float", "FranchiseCode", "Bank", "BankState",
            "RevLineCr", "Term", "crisis"
        ]

        # Ensure the data is formatted correctly for prediction
        df_data = pd.DataFrame([loan_data])
        df_data = df_data[feature_order]

        # Make a prediction using the trained LGBM model
        prediction = model.predict(df_data)

        # Return the loan eligibility result
        return {"eligibility": "Eligible for loan" if prediction[0] == 1 else "Not eligible for loan"}

    except Exception as e:
        # 8️⃣ Handle any errors during prediction
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

        

# Submission of a loan request
# POST/loans/request
@router.post("/loans/request", response_model=LoanRequest)
async def request_loan(user_id: int, loan_request: LoanRequest, session: Session = Depends(get_session)):
    # Retrieve the user from the database using the provided user_id
    user = session.get(User, user_id)
    # If the user does not exist, raise a 404 HTTP exception
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Create a new loan request instance using the provided loan_request data
    new_loan_request = LoanRequest(**loan_request.model_dump(exclude_unset=True))
    try:
        # Add the new loan request to the session
        session.add(new_loan_request)
        # Commit the transaction to save the new loan request in the database
        session.commit()
        # Refresh the session to get the updated loan request data  
        session.refresh(new_loan_request)  
    except Exception as e:
        # If an exception occurs during the database transaction, rollback the session and raise a 500 HTTP
        session.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    # Return the newly created loan request
    return new_loan_request

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

