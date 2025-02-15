from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: str  # Consider using EmailStr for better validation
    phone_no: str
    password: str
    confirm_password: str
    role_id: int  # Default role for customers

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone_no: str
    role_id: int
    is_active: bool

    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2

class UserLogin(BaseModel):
    email: str  # Consider using EmailStr for better validation
    password: str