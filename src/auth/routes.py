from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import db, utils
from . import schemas, models
from ..profiles import models as profile_models
from ..profiles import schemas as profile_schemas

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    # 1. Check if user already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Hash the password
    hashed_password = utils.hash_password(user.password)
    
    # 3. Determine role from email domain
    email_domain = user.email.split('@')[-1]
    role = "patient" # Default role
    if email_domain == "doctor.com":
        role = "doctor"
    elif email_domain == "pharmacist.com":
        role = "pharmacist"
    elif email_domain == "asha.com":
        role = "asha_worker"

    # 4. Create the main user entry
    new_user = models.User(email=user.email, hashed_password=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Create the specific profile entry based on the role
    if role == "doctor":
        profile_data = profile_schemas.DoctorCreate(full_name=user.full_name)
        new_profile = profile_models.Doctor(**profile_data.dict(), user_id=new_user.id)
    elif role == "pharmacist":
        profile_data = profile_schemas.PharmacistCreate(full_name=user.full_name)
        new_profile = profile_models.Pharmacist(**profile_data.dict(), user_id=new_user.id)
    elif role == "asha_worker":
        profile_data = profile_schemas.ASHAWorkerCreate(full_name=user.full_name)
        new_profile = profile_models.ASHAWorker(**profile_data.dict(), user_id=new_user.id)
    else: # Default to patient
        profile_data = profile_schemas.PatientCreate(full_name=user.full_name)
        new_profile = profile_models.Patient(**profile_data.dict(), user_id=new_user.id)

    db.add(new_profile)
    db.commit()
    
    return new_user

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(db.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
        
    if not utils.verify_password(user_credentials.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )

    # In a production app, you would create and return a JWT token here.
    # For the demo, a simple success message is sufficient.
    return {"status": "success", "user_id": db_user.id, "role": db_user.role}