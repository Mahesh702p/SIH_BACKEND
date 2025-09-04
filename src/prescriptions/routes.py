from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import db
from ..auth import models as auth_models
from ..auth.dependencies import role_checker
from . import models, schemas

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Prescription)
def create_prescription(
    payload: schemas.PrescriptionCreate,
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["doctor"]))
):
    new_p = models.Prescription(
        appointment_id=payload.appointment_id,
        doctor_id=current_user.doctor_profile.doctor_id,
        patient_id=payload.patient_id,
        notes=payload.notes,
        medications=payload.medications,
    )
    db.add(new_p)
    db.commit(); db.refresh(new_p)
    return new_p

@router.get("/me", response_model=list[schemas.Prescription])
def my_prescriptions(
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["patient", "asha_worker"]))
):
    return db.query(models.Prescription).filter(models.Prescription.patient_id == current_user.patient_profile.patient_id).all()

