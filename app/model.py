# credit_prototype/app/model.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Main table for microcredit applications
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    income = Column(Float, nullable=False)
    employment_status = Column(String, nullable=False)  # e.g., "Employed", "Unemployed"
    previous_credit_score = Column(Float, default=0.0)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    # Scoring result and approval status
    score = Column(Float)
    approved = Column(Boolean)

    # Reference to blockchain contract (optional)
    tx_hash = Column(String)

    # Relationship with evaluation history
    history = relationship("CreditHistory", back_populates="application")


# Table to store scoring history (traceability)
class CreditHistory(Base):
    __tablename__ = "credit_history"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    message = Column(String)  # Description or comment of the event
    score = Column(Float)

    application = relationship("Application", back_populates="history")
    
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String(8), unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)

