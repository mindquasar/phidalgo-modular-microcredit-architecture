
import joblib
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, ".\model")

lgbm_model = joblib.load(os.path.join(model_path, "lgbm_model.pkl"))
label_encoders = joblib.load(os.path.join(model_path, "label_encoders.pkl"))
train_columns = joblib.load(os.path.join(model_path, "train_columns.pkl"))
df_train = joblib.load(os.path.join(model_path, "df_train.pkl"))

from .preprocessing import process_and_score_single_row
    
def evaluate_credit(application):
    app_mapped = {
        "person_age": application["age"],
        "person_income": application["income"],
        "person_home_ownership": application["person_home_ownership"],
        "person_emp_length": application["person_emp_length"],
        "loan_intent": application["loan_intent"],
        "loan_grade": application["loan_grade"],
        "loan_ammt": application["loan_ammt"],
        "loan_int_rate": application["loan_int_rate"],
        "loan_percent_income": application["loan_percent_income"],
        "cb_person_default_on_file": application["cb_person_default_on_file"],
        "cb_person_cred_hist_length": application["cb_person_cred_hist_length"]
    }

    X_one_row = pd.DataFrame([app_mapped])

    resultado = process_and_score_single_row(
        X_one_row,
        lgbm_model,
        df_train,
        train_columns,
        label_encoders
    )

    approved = resultado['fico_score'] >= 620
    return approved, resultado['fico_score'], resultado['risk_segment']

