# credit_prototype/app/crud.py

from sqlalchemy.orm import Session
from . import model, schemas

def create_application(db: Session, data: schemas.ApplicationCreate):
    new_app = model.Application(
        name=data.name,
        age=data.age,
        income=data.income,
        employment_status=data.employment_status,
        previous_credit_score=data.previous_credit_score,
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

def update_application_result(db: Session, app_id: int, score: float, approved: bool, tx_hash: str = None):
    app = db.query(model.Application).filter(model.Application.id == app_id).first()
    app.score = score
    app.approved = approved
    if tx_hash:
        app.tx_hash = tx_hash
    db.commit()
    db.refresh(app)
    return app

def log_event(db: Session, app_id: int, message: str, score: float = None):
    event = model.CreditHistory(
        application_id=app_id,
        message=message,
        score=score
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_application_by_id(db: Session, app_id: int):
    return db.query(model.Application).filter(model.Application.id == app_id).first()
