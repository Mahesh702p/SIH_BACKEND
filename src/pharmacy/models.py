from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    pharmacist_id = Column(Integer, ForeignKey("pharmacists.pharmacist_id"))

    # Add back_populates and lazy="joined"
    pharmacist = relationship("Pharmacist", back_populates="pharmacy", lazy="joined")
    medicines = relationship("Medicine", back_populates="pharmacy")

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))

    # Add back_populates
    pharmacy = relationship("Pharmacy", back_populates="medicines")