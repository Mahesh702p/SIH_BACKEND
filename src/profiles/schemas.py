from pydantic import BaseModel, Field
import datetime

# --- Patient Schemas ---
class PatientBase(BaseModel):
    full_name: str
    date_of_birth: datetime.date | None = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    # This line tells Pydantic that 'patient_id' corresponds to the 'id' attribute
    patient_id: int = Field(alias="id")
    user_id: int
    class Config:
        from_attributes = True

# --- Doctor Schemas ---
class DoctorBase(BaseModel):
    full_name: str
    specialization: str | None = None

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    # This line tells Pydantic that 'doctor_id' corresponds to the 'id' attribute
    doctor_id: int = Field(alias="id")
    user_id: int
    class Config:
        from_attributes = True

# --- Pharmacist Schemas ---
class PharmacistBase(BaseModel):
    full_name: str
    pharmacy_name: str | None = None

class PharmacistCreate(PharmacistBase):
    pass

class Pharmacist(PharmacistBase):
    # This line tells Pydantic that 'pharmacist_id' corresponds to the 'id' attribute
    pharmacist_id: int = Field(alias="id")
    user_id: int
    class Config:
        from_attributes = True

# --- ASHAWorker Schemas ---
class ASHAWorkerBase(BaseModel):
    full_name: str
    village_assigned: str | None = None

class ASHAWorkerCreate(ASHAWorkerBase):
    pass

class ASHAWorker(ASHAWorkerBase):
    # This line tells Pydantic that 'asha_worker_id' corresponds to the 'id' attribute
    asha_worker_id: int = Field(alias="id")
    user_id: int
    class Config:
        from_attributes = True