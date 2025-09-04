from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_profile_id = Column(Integer, ForeignKey("doctors.doctor_id"))
    patient_profile_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=True)
    
    appointment_datetime = Column(DateTime, nullable=False)
    status = Column(String, default="available", nullable=False)

    # Make the relationships more explicit using foreign_keys
    doctor = relationship("Doctor", back_populates="appointments", foreign_keys=[doctor_profile_id])
    patient = relationship("Patient", back_populates="appointments", foreign_keys=[patient_profile_id])