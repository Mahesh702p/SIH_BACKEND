from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..db import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    notes = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)  # e.g., JSON string or comma-separated for MVP
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    doctor = relationship("Doctor", foreign_keys=[doctor_id])
    patient = relationship("Patient", foreign_keys=[patient_id])