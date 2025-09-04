from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..auth.dependencies import role_checker

router = APIRouter()

class SymptomInput(BaseModel):
    fever: bool | None = None
    cough: bool | None = None
    sore_throat: bool | None = None

@router.post("/check")
def check_symptoms(payload: SymptomInput, current_user = Depends(role_checker(allowed_roles=["patient", "asha_worker", "doctor"]))):
    score = sum(int(bool(x)) for x in [payload.fever, payload.cough, payload.sore_throat])
    if score >= 2:
        return {"assessment": "Likely respiratory infection", "advice": "Consult a doctor; rest and hydrate."}
    return {"assessment": "Mild symptoms", "advice": "Monitor at home; consult if worsening."}

