from pydantic import BaseModel, Field

# --- Medicine Schemas (No nested data needed here) ---
class MedicineBase(BaseModel):
    name: str
    quantity: int

class MedicineCreate(MedicineBase):
    pass

class Medicine(MedicineBase):
    medicine_id: int = Field(alias="id")
    pharmacy_id: int

    class Config:
        from_attributes = True

# --- Updates ---
class MedicineQuantityUpdate(BaseModel):
    quantity: int

# --- Pharmacy Schemas (Will include a list of medicines) ---
class PharmacyBase(BaseModel):
    name: str
    location: str

class PharmacyCreate(PharmacyBase):
    pass

class Pharmacy(PharmacyBase):
    pharmacy_id: int = Field(alias="id")
    pharmacist_id: int
    medicines: list[Medicine] = [] # Nest the medicine list in the response

    class Config:
        from_attributes = True