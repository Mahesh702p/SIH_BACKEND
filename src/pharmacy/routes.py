from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import db
from . import schemas
from . import models as pharmacy_models
from ..auth import models as auth_models
from ..auth.dependencies import role_checker

router = APIRouter(
    prefix="/pharmacies",
    tags=["Pharmacies"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Pharmacy)
def create_pharmacy(
    pharmacy: schemas.PharmacyCreate,
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["pharmacist"]))
):
    """
    Creates a new pharmacy.
    - **Security**: Only accessible by users with the 'pharmacist' role.
    - The pharmacy is automatically linked to the logged-in pharmacist.
    """
    new_pharmacy = pharmacy_models.Pharmacy(
        **pharmacy.dict(), 
        pharmacist_id=current_user.pharmacist_profile.pharmacist_id
    )
    db.add(new_pharmacy)
    db.commit()
    db.refresh(new_pharmacy)
    return new_pharmacy

@router.post("/{pharmacy_id}/medicines", status_code=status.HTTP_201_CREATED, response_model=schemas.Medicine)
def add_medicine_to_inventory(
    pharmacy_id: int, 
    medicine: schemas.MedicineCreate,
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["pharmacist"]))
):
    """
    Adds a new medicine to a specific pharmacy's inventory.
    - **Security**: Only accessible by pharmacists.
    - **Ownership Check**: A pharmacist can only add medicine to their own pharmacy.
    """
    pharmacy = db.query(pharmacy_models.Pharmacy).filter(pharmacy_models.Pharmacy.id == pharmacy_id).first()
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")
    
    if pharmacy.pharmacist_id != current_user.pharmacist_profile.pharmacist_id:
        raise HTTPException(status_code=403, detail="Not authorized to add medicine to this pharmacy")

    new_medicine = pharmacy_models.Medicine(**medicine.dict(), pharmacy_id=pharmacy_id)
    db.add(new_medicine)
    db.commit()
    db.refresh(new_medicine)
    return new_medicine

@router.get("/{pharmacy_id}/medicines", response_model=List[schemas.Medicine])
def get_pharmacy_inventory(pharmacy_id: int, db: Session = Depends(db.get_db)):
    """
    Gets the medicine stock for a specific pharmacy.
    - This is a public endpoint for patients to use.
    """
    medicines = db.query(pharmacy_models.Medicine).filter(pharmacy_models.Medicine.pharmacy_id == pharmacy_id).all()
    return medicines

@router.get("/pharmacist/me", response_model=List[schemas.Pharmacy])
def get_my_pharmacies(
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["pharmacist"]))
):
    """
    Gets a list of pharmacies owned by the currently logged-in pharmacist.
    - **Security**: Protected endpoint for 'pharmacist' roles only.
    """
    pharmacies = db.query(pharmacy_models.Pharmacy).filter(
        pharmacy_models.Pharmacy.pharmacist_id == current_user.pharmacist_profile.pharmacist_id
    ).all()
    return pharmacies


@router.put("/{pharmacy_id}/medicines/{medicine_id}", response_model=schemas.Medicine)
def update_medicine_quantity(
    pharmacy_id: int,
    medicine_id: int,
    payload: schemas.MedicineQuantityUpdate,
    db: Session = Depends(db.get_db),
    current_user: auth_models.User = Depends(role_checker(allowed_roles=["pharmacist"]))
):
    """
    Updates the stock quantity of a medicine in a pharmacy.
    - **Security**: Only pharmacists can update.
    - **Ownership Check**: Pharmacist must own the pharmacy.
    """
    pharmacy = db.query(pharmacy_models.Pharmacy).filter(pharmacy_models.Pharmacy.id == pharmacy_id).first()
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    if pharmacy.pharmacist_id != current_user.pharmacist_profile.pharmacist_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this pharmacy inventory")

    medicine = db.query(pharmacy_models.Medicine).filter(
        pharmacy_models.Medicine.id == medicine_id,
        pharmacy_models.Medicine.pharmacy_id == pharmacy_id
    ).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found in this pharmacy")

    medicine.quantity = payload.quantity
    db.commit()
    db.refresh(medicine)
    return medicine