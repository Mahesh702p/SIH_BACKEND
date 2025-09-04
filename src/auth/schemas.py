from pydantic import BaseModel, Field
import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    birthdate: datetime.date
    gender: str

class UserCreate(UserBase):
    password: str
    role: str # User now provides their role during signup

class User(UserBase):
    user_id: int = Field(alias="id")
    role: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class UserInDBBase(BaseModel):
    user_id: int = Field(alias="id")
    first_name: str
    last_name: str
    username: str
    email: str | None = None
    role: str

    class Config:
        from_attributes = True