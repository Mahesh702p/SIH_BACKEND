from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base

class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    # This links the pharmacy to a user who is a pharmacist
    pharmacist_id = Column(Integer, ForeignKey("users.id"))


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    # This links the medicine to a specific pharmacy
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))