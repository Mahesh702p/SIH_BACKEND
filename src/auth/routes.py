from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import db, utils
from . import schemas, models
from ..profiles import models as profile_models
from ..config import settings
from datetime import datetime, timedelta
import hmac, hashlib, base64
from .dependencies import get_current_user

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


@router.get("/me", response_model=schemas.User)
def me(current_user: models.User = Depends(get_current_user)):
    """Return the current authenticated user (includes role)."""
    return current_user


@router.get("/debug/all-data")
def get_all_data(db: Session = Depends(db.get_db)):
    """Returns all rows from major tables. Protect in production."""
    users = db.query(models.User).all()
    doctors = db.query(profile_models.Doctor).all()
    patients = db.query(profile_models.Patient).all()
    pharmacists = db.query(profile_models.Pharmacist).all()
    ashas = db.query(profile_models.ASHAWorker).all()
    # defer appointment/pharmacy import to avoid circulars
    from ..appointment.models import Appointment
    from ..pharmacy.models import Pharmacy, Medicine
    appointments = db.query(Appointment).all()
    pharmacies = db.query(Pharmacy).all()
    medicines = db.query(Medicine).all()
    # naive serialization
    def serialize(obj):
        d = obj.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return d
    return {
        "users": [serialize(u) for u in users],
        "doctors": [serialize(x) for x in doctors],
        "patients": [serialize(x) for x in patients],
        "pharmacists": [serialize(x) for x in pharmacists],
        "asha_workers": [serialize(x) for x in ashas],
        "appointments": [serialize(x) for x in appointments],
        "pharmacies": [serialize(x) for x in pharmacies],
        "medicines": [serialize(x) for x in medicines],
    }


@router.post("/video/token")
def create_agora_token(channel: str, uid: str, role: str = "publisher", expire_minutes: int = 60):
    """
    Minimal token generator for Agora RTC using App ID/Certificate.
    For demo only; use official SDKs for production security.
    """
    if not settings.Agora_APP_ID if False else None:
        pass
    app_id = settings.AGORA_APP_ID
    app_cert = settings.AGORA_APP_CERTIFICATE
    if not app_id or not app_cert:
        raise HTTPException(status_code=500, detail="Agora credentials not configured")
    # Simple token format (NOT official) as placeholder; replace with official builder if added
    expire_ts = int((datetime.utcnow() + timedelta(minutes=expire_minutes)).timestamp())
    msg = f"{app_id}:{channel}:{uid}:{role}:{expire_ts}".encode()
    sig = hmac.new(app_cert.encode(), msg, hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(msg + b"." + sig).decode()
    return {"token": token, "appId": app_id, "channel": channel, "uid": uid, "expires": expire_ts}