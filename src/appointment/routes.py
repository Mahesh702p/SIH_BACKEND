from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import datetime

# --- Module Imports ---
from .. import db
from . import schemas
from . import models as appointment_models
from ..auth import models as auth_models
from ..profiles import models as profile_models
from ..auth.dependencies import role_checker

router = APIRouter()


# --- Endpoints ---

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Appointment)
def create_appointment_slot(
    appointment_in: schemas.AppointmentCreate,
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["doctor", "asha_worker"]))
):
    """
    Creates a new, available appointment slot.

    - **Security**: Doctors and ASHA workers can create slots.
    - The `doctor_id` is automatically assigned from the token for doctors.
    - ASHA workers may optionally provide a `doctor_profile_id`; if omitted, this will error.
    - The request body should contain the desired date and time for the slot.
    """
    appointment_datetime = datetime.datetime.combine(
        appointment_in.appointment_date, 
        appointment_in.appointment_time
    )

    if current_user.role == "doctor":
        doctor_profile = current_user.doctor_profile
    else:
        # ASHA worker must specify which doctor the slot is for
        if not appointment_in.doctor_profile_id:
            raise HTTPException(status_code=400, detail="doctor_profile_id is required for ASHA worker")
        doctor_profile = db.query(profile_models.Doctor).filter(
            profile_models.Doctor.doctor_id == appointment_in.doctor_profile_id
        ).first()
        if not doctor_profile:
            raise HTTPException(status_code=404, detail="Doctor not found")

    new_appointment = appointment_models.Appointment(
        appointment_datetime=appointment_datetime,
        doctor=doctor_profile
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    # Re-fetch the object with all relationships eagerly loaded to ensure a complete response
    created_appointment = db.query(appointment_models.Appointment).options(
        joinedload(appointment_models.Appointment.doctor).joinedload(profile_models.Doctor.user)
    ).filter(appointment_models.Appointment.id == new_appointment.id).first()
    
    return created_appointment


@router.get("/available", response_model=List[schemas.Appointment])
def get_all_available_slots(db: Session = Depends(db.get_db)):
    """
    Fetches a list of all appointment slots that are currently 'available'.

    - This is a public endpoint accessible by any user.
    """
    appointments = db.query(appointment_models.Appointment).options(
        joinedload(appointment_models.Appointment.doctor).joinedload(profile_models.Doctor.user),
        joinedload(appointment_models.Appointment.patient).joinedload(profile_models.Patient.user)
    ).filter(
        appointment_models.Appointment.status == "available"
    ).all()
    return appointments


@router.get("/doctor/me", response_model=List[schemas.Appointment])
def get_my_doctor_appointments(
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["doctor"]))
):
    """
    Fetches all appointments (available, booked, etc.) for the currently logged-in doctor.
    
    - **Security**: Protected endpoint for 'doctor' roles only.
    """
    appointments = db.query(appointment_models.Appointment).options(
        joinedload(appointment_models.Appointment.doctor).joinedload(profile_models.Doctor.user),
        joinedload(appointment_models.Appointment.patient).joinedload(profile_models.Patient.user)
    ).filter(
        appointment_models.Appointment.doctor_profile_id == current_user.doctor_profile.doctor_id
    ).all()
    return appointments


@router.get("/patient/me", response_model=List[schemas.Appointment])
def get_my_patient_appointments(
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["patient", "asha_worker"]))
):
    """
    Fetches all appointments for the currently logged-in patient.

    - **Security**: Protected endpoint for 'patient' and 'asha_worker' roles.
    """
    appointments = db.query(appointment_models.Appointment).options(
        joinedload(appointment_models.Appointment.doctor).joinedload(profile_models.Doctor.user),
        joinedload(appointment_models.Appointment.patient).joinedload(profile_models.Patient.user)
    ).filter(
        appointment_models.Appointment.patient_profile_id == current_user.patient_profile.patient_id
    ).all()
    return appointments


@router.post("/{appointment_id}/book", response_model=schemas.Appointment)
def book_appointment_slot(
    appointment_id: int,
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["patient", "asha_worker"]))
):
    """
    Books an available appointment slot for the currently logged-in patient.

    - **Security**: Protected endpoint for 'patient' and 'asha_worker' roles.
    - The `patient_id` is automatically assigned based on the logged-in user's token.
    """
    # Eagerly load the relationships for the response
    appointment_to_book = db.query(appointment_models.Appointment).options(
        joinedload(appointment_models.Appointment.doctor).joinedload(profile_models.Doctor.user)
    ).filter(
        appointment_models.Appointment.id == appointment_id
    ).first()
    
    if not appointment_to_book:
        raise HTTPException(status_code=404, detail="Appointment slot not found")
        
    if appointment_to_book.status != "available":
        raise HTTPException(status_code=400, detail="Appointment slot is already booked")
        
    appointment_to_book.patient_profile_id = current_user.patient_profile.patient_id
    appointment_to_book.status = "booked"
    db.commit()
    db.refresh(appointment_to_book)
    
    return appointment_to_book