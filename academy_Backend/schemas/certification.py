from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


class CertificationBase(BaseModel):
    """Base schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255, description="Certification name")
    deadline_date: Optional[date] = Field(None, description="Deadline date for certification")
    link: Optional[str] = Field(None, max_length=500, description="Certification link/URL")

    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Certification name cannot be empty')
        return v.strip()

    @validator('link')
    def validate_link(cls, v):
        if v and v.strip():
            return v.strip()
        return None


class CertificationCreate(CertificationBase):
    """Schema for creating new certification"""
    certification_id: str = Field(..., min_length=1, max_length=50, description="Unique certification ID")

    @validator('certification_id')
    def certification_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Certification ID cannot be empty')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "certification_id": "CERT001",
                "name": "Python Fundamentals Certification",
                "deadline_date": "2025-12-01",
                "link": "https://certification.example.com/python-fundamentals"
            }
        }


class CertificationUpdate(CertificationBase):
    """Schema for updating certification"""

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Advanced Python Certification",
                "deadline_date": "2025-12-15",
                "link": "https://certification.example.com/python-advanced"
            }
        }


class CertificationResponse(BaseModel):
    """Schema for certification response"""
    certification_id: str
    name: str
    deadline_date: Optional[date]
    link: Optional[str]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "certification_id": "CERT001",
                "name": "Python Fundamentals Certification",
                "deadline_date": "2025-12-01",
                "link": "https://certification.example.com/python-fundamentals"
            }
        }
