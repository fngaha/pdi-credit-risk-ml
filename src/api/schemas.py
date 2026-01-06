from __future__ import annotations

from pydantic import BaseModel, Field


class CreditRiskRequest(BaseModel):
    # Numériques
    duration: int = Field(..., ge=1)
    credit_amount: float = Field(..., gt=0)
    installment_commitment: int = Field(..., ge=1, le=4)
    residence_since: int = Field(..., ge=1, le=4)
    age: int = Field(..., ge=18, le=120)
    existing_credits: int = Field(..., ge=0, le=10)
    num_dependents: int = Field(..., ge=0, le=10)

    # Catégorielles (on laisse libre pour handle_unknown="ignore")
    checking_status: str
    credit_history: str
    purpose: str
    savings_status: str
    employment: str
    personal_status: str
    other_parties: str
    property_magnitude: str
    other_payment_plans: str
    housing: str
    job: str
    own_telephone: str
    foreign_worker: str


class CreditRiskResponse(BaseModel):
    label: str
    probability_bad: float
    probability_good: float
    risk_level: str
