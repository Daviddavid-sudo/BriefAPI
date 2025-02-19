from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models import User, LoanRequest
from app.database import get_session, engine
import joblib
import numpy as np


router = APIRouter()

### Routes for loan requests ###
# Load the pre-trained model for loan eligibility prediction
model = joblib.load("app/model/xgb_model.pkl")  # Ensure the model file is present in the correct path


# GET /loans/predict
@router.get("/loans/predict")
def predict_loan_eligibility(loan_id: int, session: Session = Depends(get_session)):
    # Retrieve the loan request from the database using the provided loan_id
    loan_request = session.get(LoanRequest, loan_id)
    # If the loan request does not exist, raise a 404 HTTP exception
    if not loan_request:
        raise HTTPException(status_code=404, detail="Loan request not found")
    else:
        try:
            # Convert loan request data to a dictionary
            loan_data = loan_request.model_dump()
        
            # Convert dictionary values to a numpy array
            data_array = np.array([list(loan_data.values())])
            # Make a prediction using the loaded model
            prediction = model.predict(data_array)
            # Return eligibility based on the prediction
            if prediction[0] == 1:
                return {"eligibility": "Eligible for loan"}
            else:
                return {"eligibility": "Not eligible for loan"}
        except Exception as e:
            # If an exception occurs during prediction, raise a 500 HTTP exception
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# Submission of a loan request
# POST/loans/request
@router.post("/loans/request", response_model=LoanRequest)
def request_loan(user_id: int, loan_request: LoanRequest, session: Session = Depends(get_session)):
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
def get_loan_history(user_id: int, session: Session = Depends(get_session)):
    # Execute a SQL query to select all loan requests for the given user_id
    loans = session.exec(select(LoanRequest).where(LoanRequest.user_id == user_id)).all()
    # If no loan requests are found, raise a 404 HTTP exception
    if not loans:
        raise HTTPException(status_code=404, detail="No loan requests found")
    # Return the list of loan requests
    return loans

