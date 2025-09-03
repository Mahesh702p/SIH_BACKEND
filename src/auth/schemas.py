from pydantic import BaseModel
from ..profiles.schemas import Patient, Doctor, Pharmacist, ASHAWorker

# This is the schema for creating a new user during sign-up
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

# This is the schema for the data sent during a login attempt
class UserLogin(BaseModel):
    email: str
    password: str

# This is the main schema for returning user data from the API
class User(BaseModel):
    id: int
    email: str
    role: str
    
    # These optional fields will hold the nested profile data.
    # A user will only have one of these profiles populated.
    patient_profile: Patient | None = None
    doctor_profile: Doctor | None = None
    pharmacist_profile: Pharmacist | None = None
    asha_worker_profile: ASHAWorker | None = None

    class Config:
        from_attributes = True