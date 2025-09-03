from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..db import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    date_of_birth = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="patient_profile")
    
    # Add this relationship to link to appointments
    appointments = relationship("Appointment", back_populates="patient")

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    specialization = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="doctor_profile")

    # Add this relationship to link to appointments
    appointments = relationship("Appointment", back_populates="doctor")

class Pharmacist(Base):
    __tablename__ = "pharmacists"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    pharmacy_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="pharmacist_profile")

class ASHAWorker(Base):
    __tablename__ = "asha_workers"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    village_assigned = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="asha_worker_profile")