from pydantic import BaseModel, Field
import datetime
from ..profiles.schemas import Doctor, Patient # Import full profile schemas for richer responses

# --- Base and Create Schemas ---

class AppointmentBase(BaseModel):
    # Base schema no longer needs any fields as they are context-dependent

    class Config:
        from_attributes = True

class AppointmentCreate(AppointmentBase):
    """Schema for creating a slot. Doctor ID is taken from the token unless provided by ASHA."""
    appointment_date: datetime.date
    appointment_time: datetime.time
    doctor_profile_id: int | None = None

class AppointmentUpdate(AppointmentBase):
    """Schema for updating an appointment's status."""
    status: str


# --- Read Schemas (for API Responses) ---

class Appointment(AppointmentBase):
    """The full appointment schema for API responses."""
    appointment_id: int = Field(alias="id") # Renamed 'id' to 'appointment_id'
    appointment_datetime: datetime.datetime
    status: str
    
    # Nest the full profile information in the response for convenience
    doctor: Doctor | None = None
    patient: Patient | None = None