from pydantic import BaseModel
import datetime

# 1. Base Schema
class AppointmentBase(BaseModel):
    doctor_id: int
    appointment_datetime: datetime.datetime

# 2. Schema for Creating Data
class AppointmentCreate(AppointmentBase):
    pass

# 3. Schema for Reading Data
class Appointment(AppointmentBase):
    id: int
    patient_id: int | None = None
    status: str

class AppointmentBook(BaseModel):
    patient_id: int

    class Config:
        from_attributes = True