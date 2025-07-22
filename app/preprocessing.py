import pandas as pd
import numpy as np

def process_and_score_single_row(X_row, model, df_train, train_columns, label_encoders):
    # Aplicar encoding a las columnas categóricas usando los label_encoders
    for col, le in label_encoders.items():
        if col in X_row.columns:
            X_row[col] = le.transform(X_row[col])

    # Rellenar columnas faltantes con valores por defecto
    for col in train_columns:
        if col not in X_row.columns:
            X_row[col] = 0

    # Asegurar el orden de columnas
    X_row = X_row[train_columns]

    # Predecir probabilidad
    default_proba = model.predict_proba(X_row)[0][1]

    # Convertir a FICO-style score
    offset = 600
    factor = 20 / np.log(10)
    fico_score = int(offset - factor * np.log(default_proba / (1 - default_proba)))

    # Asignar segmento de riesgo
    if fico_score < 580:
        risk_segment = "Riesgo alto"
    elif fico_score < 670:
        risk_segment = "Riesgo medio"
    else:
        risk_segment = "Riesgo bajo"

    return {
        "default_proba": default_proba,
        "fico_score": fico_score,
        "risk_segment": risk_segment
    }
