from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..db import Base

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    managed_by_asha_id = Column(Integer, ForeignKey("asha_workers.asha_worker_id"), nullable=True)
    
    user = relationship("User", back_populates="patient_profile", foreign_keys=[user_id])
    
    # Corrected the foreign_keys string format
    appointments = relationship("Appointment", back_populates="patient", foreign_keys="Appointment.patient_profile_id")
    managing_asha = relationship("ASHAWorker", back_populates="patients", foreign_keys=[managed_by_asha_id])

class Doctor(Base):
    __tablename__ = "doctors"
    doctor_id = Column(Integer, primary_key=True, index=True)
    specialization = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="doctor_profile", foreign_keys=[user_id])
    
    # Corrected the foreign_keys string format
    appointments = relationship("Appointment", back_populates="doctor", foreign_keys="Appointment.doctor_profile_id")

class Pharmacist(Base):
    __tablename__ = "pharmacists"
    pharmacist_id = Column(Integer, primary_key=True, index=True)
    pharmacy_name = Column(String) # This can be the primary pharmacy name
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="pharmacist_profile", lazy="joined")
    
    # Add this relationship to link a pharmacist to their pharmacy
    pharmacy = relationship("Pharmacy", back_populates="pharmacist", uselist=False)


class ASHAWorker(Base):
    __tablename__ = "asha_workers"
    asha_worker_id = Column(Integer, primary_key=True, index=True)
    village_assigned = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="asha_worker_profile", lazy="joined")
    
    # Add this relationship to get a list of patients for an ASHA worker
    patients = relationship("Patient", back_populates="managing_asha", foreign_keys="Patient.managed_by_asha_id")