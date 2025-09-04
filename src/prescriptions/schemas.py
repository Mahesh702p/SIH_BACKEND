from pydantic import BaseModel, Field
from typing import Optional

class PrescriptionCreate(BaseModel):
    appointment_id: Optional[int] = None
    patient_id: int
    notes: Optional[str] = None
    medications: Optional[str] = None

class Prescription(BaseModel):
    prescription_id: int = Field(alias="id")
    appointment_id: int | None
    doctor_id: int
    patient_id: int
    notes: str | None
    medications: str | None

    class Config:
        from_attributes = True