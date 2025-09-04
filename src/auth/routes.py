from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import db, utils
from . import schemas, models
from ..profiles import models as profile_models

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    hashed_password = utils.hash_password(user.password)
    
    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role,
        first_name=user.first_name,
        last_name=user.last_name,
        birthdate=user.birthdate,
        gender=user.gender
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create the specific profile entry
    if user.role == "doctor":
        new_profile = profile_models.Doctor(user_id=new_user.id)
    elif user.role == "pharmacist":
        new_profile = profile_models.Pharmacist(user_id=new_user.id)
    elif user.role == "asha_worker":
        new_profile = profile_models.ASHAWorker(user_id=new_user.id)
    else: # Default to patient
        new_profile = profile_models.Patient(user_id=new_user.id)

    db.add(new_profile)
    db.commit()
    
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = utils.create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}