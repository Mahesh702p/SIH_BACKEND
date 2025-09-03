from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import db  # This line is now corrected to match your filename
from . import schemas
from . import models

# Create the router
router = APIRouter()

# Dependency for getting a database session
def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/", response_model=schemas.Appointment)
def create_appointment_slot(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    """
    Endpoint for a doctor to create a new, available appointment slot.
    """
    new_appointment = models.Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

@router.get("/doctor/{doctor_id}/available", response_model=List[schemas.Appointment])
def get_available_slots(doctor_id: int, db: Session = Depends(get_db)):
    """
    Endpoint for a patient to see all available slots for a specific doctor.
    """
    appointments = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.status == "available"
    ).all()
    return appointments

# Note: For the 'book' endpoint, let's create a simple schema for the request body
# Add this class to your src/appointment/schemas.py file
# class AppointmentBook(BaseModel):
#     patient_id: int

@router.post("/{appointment_id}/book", response_model=schemas.Appointment)
def book_appointment_slot(appointment_id: int, patient_id: int, db: Session = Depends(get_db)):
    """
    Endpoint for a patient to book a specific, available appointment slot.
    """
    appointment_to_book = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    
    if not appointment_to_book:
        raise HTTPException(status_code=404, detail="Appointment slot not found")
        
    if appointment_to_book.status != "available":
        raise HTTPException(status_code=400, detail="Appointment slot is already booked")
        
    appointment_to_book.patient_id = patient_id
    appointment_to_book.status = "booked"
    db.commit()
    db.refresh(appointment_to_book)
    return appointment_to_book