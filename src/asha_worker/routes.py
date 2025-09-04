from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import db, utils
from ..auth import schemas as auth_schemas
from ..auth import models as auth_models
from ..profiles import models as profile_models
from ..profiles import schemas as profile_schemas
from ..appointment import models as appointment_models
from ..auth.dependencies import role_checker

router = APIRouter()


@router.get("/me/patients", response_model=List[profile_schemas.Patient])
def get_my_managed_patients(
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["asha_worker"]))
):
    """
    Fetches a list of all patients managed by the currently logged-in ASHA worker.
    - **Security**: Protected endpoint for 'asha_worker' roles only.
    """
    return current_user.asha_worker_profile.patients

@router.post("/onboard-patient", status_code=status.HTTP_201_CREATED, response_model=profile_schemas.Patient)
def onboard_new_patient(
    patient_details: auth_schemas.UserCreate,
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["asha_worker"]))
):
    """
    Creates a new user and patient profile on behalf of a patient (Assisted Onboarding).
    - **Security**: Protected endpoint for 'asha_worker' roles only.
    - The new patient is automatically assigned to the logged-in ASHA worker.
    """
    # This logic is similar to the main /auth/signup endpoint
    db_user = db.query(auth_models.User).filter(auth_models.User.username == patient_details.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = utils.hash_password(patient_details.password)
    
    new_user = auth_models.User(
        username=patient_details.username,
        hashed_password=hashed_password,
        role="patient", # Role is fixed to 'patient'
        first_name=patient_details.first_name,
        last_name=patient_details.last_name,
        birthdate=patient_details.birthdate,
        gender=patient_details.gender
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_patient_profile = profile_models.Patient(
        user_id=new_user.id,
        managed_by_asha_id=current_user.asha_worker_profile.asha_worker_id
    )
    db.add(new_patient_profile)
    db.commit()
    db.refresh(new_patient_profile)
    
    return new_patient_profile