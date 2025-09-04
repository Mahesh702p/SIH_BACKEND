from pydantic import BaseModel, Field, computed_field
import datetime
from ..auth.schemas import UserInDBBase # Import the base user schema

# --- Patient Schemas ---
class PatientBase(BaseModel):
    date_of_birth: datetime.date | None = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    patient_id: int
    user_id: int
    user: UserInDBBase

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
        
    class Config:
        from_attributes = True

# --- Doctor Schemas ---
class DoctorBase(BaseModel):
    specialization: str | None = None

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    doctor_id: int
    user_id: int
    user: UserInDBBase

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    class Config:
        from_attributes = True

# --- Pharmacist Schemas ---
class PharmacistBase(BaseModel):
    pharmacy_name: str | None = None

class PharmacistCreate(PharmacistBase):
    pass

class Pharmacist(PharmacistBase):
    pharmacist_id: int
    user_id: int
    user: UserInDBBase

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    class Config:
        from_attributes = True

# --- ASHAWorker Schemas ---
class ASHAWorkerBase(BaseModel):
    village_assigned: str | None = None

class ASHAWorkerCreate(ASHAWorkerBase):
    pass

class ASHAWorker(ASHAWorkerBase):
    asha_worker_id: int
    user_id: int
    user: UserInDBBase

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    class Config:
        from_attributes = True