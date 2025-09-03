from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import db
from . import schemas
from . import models

# Create the router
router = APIRouter()

# Dependency for getting a database session
def get_db():
    database = db.SessionLocal()  # Changed variable name from db to database to avoid conflict
    try:
        yield database
    finally:
        database.close()

@router.post("/", response_model=schemas.Pharmacy)
def create_pharmacy(pharmacy: schemas.PharmacyCreate, database: Session = Depends(get_db)):
    """
    Endpoint to create a new pharmacy, linked to a pharmacist.
    """
    new_pharmacy = models.Pharmacy(**pharmacy.dict())
    database.add(new_pharmacy)
    database.commit()
    database.refresh(new_pharmacy)
    return new_pharmacy

@router.post("/{pharmacy_id}/medicines", response_model=schemas.Medicine)
def add_medicine_to_inventory(pharmacy_id: int, medicine: schemas.MedicineCreate, db: Session = Depends(get_db)):
    """
    Endpoint to add a new medicine to a specific pharmacy's inventory.
    """
    new_medicine = models.Medicine(**medicine.dict(), pharmacy_id=pharmacy_id)
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    return new_medicine

@router.get("/{pharmacy_id}/medicines", response_model=List[schemas.Medicine])
def get_pharmacy_inventory(pharmacy_id: int, db: Session = Depends(get_db)):
    """
    Endpoint for a patient to view the medicine stock of a specific pharmacy.
    """
    medicines = db.query(models.Medicine).filter(models.Medicine.pharmacy_id == pharmacy_id).all()
    if not medicines:
        raise HTTPException(status_code=404, detail="No medicines found for this pharmacy")
    return medicines

@router.put("/medicines/{medicine_id}", response_model=schemas.Medicine)
def update_medicine_quantity(medicine_id: int, quantity: int, db: Session = Depends(get_db)):
    """

    Endpoint for a pharmacist to update the stock quantity of a medicine.
    """
    medicine_to_update = db.query(models.Medicine).filter(models.Medicine.id == medicine_id).first()
    
    if not medicine_to_update:
        raise HTTPException(status_code=404, detail="Medicine not found")
        
    medicine_to_update.quantity = quantity
    db.commit()
    db.refresh(medicine_to_update)
    return medicine_to_update