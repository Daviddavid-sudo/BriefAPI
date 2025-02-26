from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models import User, loan_requests
from app.database import engine

from app.database import get_session
import joblib
import numpy as np
import lightgbm
import pandas as pd
import joblib
import pickle

router = APIRouter()

#model = joblib.load("app/final_model_pipeline.pkl")
with open("app/final_model_pipeline.pkl", "rb") as file:
    model = pickle.load(file)


@router.post("/loans/request")
async def request_loan_and_predict(loan_request: loan_requests):

    loan_data = {
        "GrAppv": [loan_request.GrAppv],
        "Term": [loan_request.Term],
        "State": [loan_request.State],
        "NAICS_Sectors": [loan_request.NAICS_Sectors],
        "New": [loan_request.New],
        "Franchise": [loan_request.Franchise],
        "NoEmp" : [loan_request.NoEmp],
        "RevLineCr": [loan_request.RevLineCr],
        "LowDoc": [loan_request.LowDoc],
        "Rural": [loan_request.Rural]        
    }
    
    df_data = pd.DataFrame(loan_data)
    df_data["GrAppv"] = df_data["GrAppv"].astype("float32")
    df_data["Term"] = df_data["Term"].astype("float32")
    df_data["State"] = df_data["State"].astype("str")
    df_data["NAICS_Sectors"] = df_data["NAICS_Sectors"].astype("str")
    df_data["New"] = df_data["New"].astype("str")
    df_data["Franchise"] = df_data["Franchise"].astype("float")
    df_data["NoEmp"] = df_data["NoEmp"].astype("float32")
    df_data["RevLineCr"] = df_data["RevLineCr"].astype("str")
    df_data["LowDoc"] = df_data["LowDoc"].astype("str")
    df_data["Rural"] = df_data["Rural"].astype("str")

    prediction = model.predict(df_data)
    loan_request.prediction = "True" if prediction[0] == 1 else False
    eligibility_message = "Your loan request has been accepted." if loan_request.prediction else "Your loan request has not been accepted."


    return {
            "message": eligibility_message
        }
    

# History of loan requests
# GET /loans/history
@router.get("/loans/history")
async def get_loan_history(id: int, session: Session = Depends(get_session)):
    # Execute a SQL query to select all loan requests for the given user_id
    loans = session.exec(select(loan_requests).where(loan_requests.id == id)).all()
    # If no loan requests are found, raise a 404 HTTP exception
    if not loans:
        raise HTTPException(status_code=404, detail="No loan requests found")
    # Return the list of loan requests
    return loans





