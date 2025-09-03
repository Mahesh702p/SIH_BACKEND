from pydantic import BaseModel

# --- Pharmacy Schemas ---

class PharmacyBase(BaseModel):
    name: str
    location: str

class PharmacyCreate(PharmacyBase):
    pharmacist_id: int

class Pharmacy(PharmacyBase):
    id: int
    pharmacist_id: int

    class Config:
        from_attributes = True

# --- Medicine Schemas ---

class MedicineBase(BaseModel):
    name: str
    quantity: int

class MedicineCreate(MedicineBase):
    pass

class Medicine(MedicineBase):
    id: int
    pharmacy_id: int

    class Config:
        from_attributes = True