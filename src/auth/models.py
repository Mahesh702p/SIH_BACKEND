from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, index=True)

    # These lines establish the two-way relationship
    patient_profile = relationship("Patient", back_populates="user", uselist=False)
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    pharmacist_profile = relationship("Pharmacist", back_populates="user", uselist=False)
    asha_worker_profile = relationship("ASHAWorker", back_populates="user", uselist=False)