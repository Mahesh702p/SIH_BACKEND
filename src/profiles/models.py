from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..db import Base

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="patient_profile", foreign_keys=[user_id])
    appointments = relationship("Appointment", back_populates="patient", foreign_keys="[Appointment.patient_profile_id]")

class Doctor(Base):
    __tablename__ = "doctors"
    doctor_id = Column(Integer, primary_key=True, index=True)
    specialization = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="doctor_profile", foreign_keys=[user_id])
    appointments = relationship("Appointment", back_populates="doctor", foreign_keys="[Appointment.doctor_profile_id]")

class Pharmacist(Base):
    __tablename__ = "pharmacists"
    pharmacist_id = Column(Integer, primary_key=True, index=True)
    pharmacy_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="pharmacist_profile", foreign_keys=[user_id])

class ASHAWorker(Base):
    __tablename__ = "asha_workers"
    asha_worker_id = Column(Integer, primary_key=True, index=True)
    village_assigned = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="asha_worker_profile", foreign_keys=[user_id])