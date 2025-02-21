from app.schemas.loans import LoanRequest

def convert_loan_request(loan: LoanRequest) -> dict:
    """
    Converts a LoanRequest object into a dictionary formatted for the LGBM model.

    Args:
        loan (LoanRequest): LoanRequest object from the database.

    Returns:
        dict: Data formatted with the feature names expected by the model.
    """
    # Mapping between LoanRequest fields and the model's dataset features
    feature_mapping = {
        "state": "State",
        "naics": "NAICS",
        "year": "ApprovalFY",
        "urbanrural": "UrbanRural",
        "lowdoc": "LowDoc",
        "franchisecode": "FranchiseCode",
        "bank": "Bank",
        "bankstate": "BankState",
        "revline": "RevLineCr",
        "term": "Term",
        "amount": "bank_loan_float",  # Convert Amount to bank_loan_float
        "sba_guaranteed": "SBA_loan_float",  # Convert SBA_Guaranteed to SBA_loan_float
        "crisis": "crisis"  # Directly use the 'crisis' field from LoanRequest, default is 0
    }

    # Ensure all expected columns are present
    formatted_data = {model_feature: getattr(loan, db_field) for db_field, model_feature in feature_mapping.items()}

    return formatted_data
