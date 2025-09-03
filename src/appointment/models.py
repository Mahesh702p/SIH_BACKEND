from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship  # Make sure relationship is imported
from ..db import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id")) # Correct this to doctors.id
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True) # Correct this to patients.id
    
    appointment_datetime = Column(DateTime, nullable=False)
    status = Column(String, default="available", nullable=False)

    # Add these two relationship links
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")