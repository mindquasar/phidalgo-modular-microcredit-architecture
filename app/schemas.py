# credit_prototype/app/schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 1. Incoming credit application from frontend or external API
class CreditApplicationIn(BaseModel):
    client_id: str = Field(..., description="Unique client identifier")
    income: float = Field(..., gt=0, description="Client's monthly income")
    age: int = Field(..., ge=18, le=100, description="Applicant's age")
    credit_score: int = Field(..., ge=0, le=1000, description="Previous credit score")
    employment_status: str = Field(..., description="Employment status: Employed, Unemployed, etc.")
    requested_amount: float = Field(..., gt=0, description="Requested microcredit amount")

# 2. Scoring result returned to the user
class ScoringResult(BaseModel):
    approved: bool = Field(..., description="Credit evaluation result")
    #score: float = Field(..., ge=0.0, le=1.0, description="Calculated risk score")
    score: int = Field(..., ge=300, le=850, description="FICO-style credit score")
    risk_segment: str = Field(..., description="Risk segmentation level")
    message: Optional[str] = Field(None, description="Additional explanatory message")

# 3. Schema for DB creation (matches Application model)
class ApplicationCreate(BaseModel):
    name: str
    age: int
    income: float
    employment_status: str
    previous_credit_score: float

    # nuevos campos requeridos por el modelo
    person_home_ownership: str
    person_emp_length: float
    loan_intent: str
    loan_grade: str
    loan_ammt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_default_on_file: str
    cb_person_cred_hist_length: int
    
# 4. Response when retrieving a full application
class ApplicationOut(BaseModel):
    id: int
    name: str
    age: int
    income: float
    employment_status: str
    previous_credit_score: float
    score: Optional[float]
    approved: Optional[bool]
    tx_hash: Optional[str]
    submitted_at: datetime

    class Config:
        orm_mode = True

# 5. Event history (optional, for traceability)
class HistoryEvent(BaseModel):
    id: int
    application_id: int
    timestamp: datetime
    message: str
    score: Optional[float]

    class Config:
        orm_mode = True


class TxRequest(BaseModel):
    client: str
    amount: int
    approved: bool
    sender_address: str
