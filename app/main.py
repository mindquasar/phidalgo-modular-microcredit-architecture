from fastapi import FastAPI, HTTPException, Depends
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from app import model, schemas, crud, database, credit_scoring
from fastapi.middleware.cors import CORSMiddleware
from app import blockchain  # <-- Importa el módulo blockchain

model.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Microcredit Scoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/applications/", response_model=schemas.ScoringResult)
def submit_application(app_data: schemas.ApplicationCreate, db: Session = Depends(database.get_db)):
    try:
        # Step 1: Save new application
        new_app = crud.create_application(db, app_data)
        print("Datos recibidos:", app_data.dict())

        # Step 2: Evaluate using scoring logic
        approved, fico_score, risk_segment = credit_scoring.evaluate_credit(app_data.dict())

        # Step 3: Log event
        crud.log_event(db, new_app.id, "Evaluation completed", fico_score)
        
        # Step 4: Prepare simulated or real blockchain transaction
        # Step 4: Prepare simulated or real blockchain transaction
        if approved:
            # Simulated: you could receive sender_address from frontend later
            simulated_sender = "0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2"
            txn = blockchain.prepare_transaction(
                client=new_app.name,
                amount=int(app_data.income),
                approved=True,
                sender_address=simulated_sender
            )
            tx_hash = f"simulated-tx-{new_app.id}"
            
            message = "Crédito aprobado y transacción en blockchain preparada."
        else:
            tx_hash = None
            if risk_segment == "Riesgo medio":
                message = "Crédito no aprobado automáticamente. Pasa a revisión manual por nivel de riesgo intermedio."
            else:
                message = "Crédito denegado automáticamente por alto riesgo."


        # Step 5: Save result
        crud.update_application_result(db, new_app.id, fico_score, approved, tx_hash)

        return schemas.ScoringResult(approved=approved, score=fico_score, risk_segment=risk_segment, message=message)

    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

        
@app.post("/prepare_tx")
def prepare_tx(req: schemas.TxRequest):
    try:
        txn = blockchain.prepare_transaction(
            client=req.client,
            amount=req.amount,
            approved=req.approved,
            sender_address=req.sender_address
        )

        # Convertir gas y gasPrice a hexadecimal
        response_tx = {
            "from": txn["from"],
            "to": txn["to"],
            "data": txn["data"],
            "gas": hex(txn["gas"]),
            "gasPrice": hex(txn["gasPrice"]),
            "value": hex(txn.get("value", 0))
        }

        return JSONResponse(content=response_tx)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to prepare tx: {str(e)}")

@app.get("/history/{application_id}", response_model=List[schemas.HistoryEvent])
def get_application_history(application_id: int, db: Session = Depends(database.get_db)):
    app_record = crud.get_application_by_id(db, application_id)
    if not app_record:
        raise HTTPException(status_code=404, detail="Not Found")
    return app_record.history

@app.get("/clients/{dni}")
def get_client_by_dni(dni: str, db: Session = Depends(database.get_db)):
    client = db.query(model.Client).filter(model.Client.dni == dni).first()
    if client:
        return {"id": client.id, "dni": client.dni, "name": client.name}
    raise HTTPException(status_code=404, detail="Client not found")
