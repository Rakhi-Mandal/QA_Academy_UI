"""
Pydantic schemas for User API
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    user_mail: EmailStr = Field(..., description="User email address")
    user_role: str = Field(..., description="Role of the user (admin/employee)")


class UserCreate(BaseModel):
    """Schema for creating a new user (and optionally employee)"""
    user_mail: EmailStr
    user_password: str
    user_role: str
    employee_id: Optional[str] = None
    employee_name: Optional[str] = None
    designation: Optional[str] = None
    pod_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_mail": "lavanya.gorrela@feuji.com",
                "user_password": "pass123",
                "user_role": "employee",
                "employee_id": "FS392",
                "employee_name": "Lavanya Gorrela",
                "designation": "Software Development Engineer in Test - I",
                "pod_id": 2
            }
        }



class UserUpdate(BaseModel):
    user_password: Optional[str] = Field(None, description="New password")
    user_role: Optional[str] = Field(None, description="Updated role")

    class Config:
        json_schema_extra = {
            "example": {
                "user_password": "newpass456",
                "user_role": "admin"
            }
        }


class UserResponse(BaseModel):
    user_id: int
    user_mail: str
    user_role: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "user_mail": "rakhi.mandal@feuji.com",
                "user_role": "employee"
            }
        }


class UserLogin(BaseModel):
    user_mail: EmailStr
    user_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_mail": "rakhi.mandal@feuji.com",
                "user_password": "password123"
            }
        }
