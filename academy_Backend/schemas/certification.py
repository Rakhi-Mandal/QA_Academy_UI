from pydantic import BaseModel, Field, validator
from typing import Optional

class CertificationBase(BaseModel):
    """Base schema with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Certification name")
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
    """Schema for creating new certification, requires ID."""
    certification_id: str = Field(..., min_length=1, max_length=50, description="Unique certification ID")

    @validator('certification_id')
    def certification_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Certification ID cannot be empty')
        return v.strip()

class CertificationUpdate(CertificationBase):
    """Schema for updating certification (all fields optional)."""
    name: Optional[str] = None
    link: Optional[str] = None

class CertificationResponse(BaseModel):
    """Schema for standard certification response."""
    certification_id: str
    name: str
    link: Optional[str]

    class Config:
        from_attributes = True

class CertificationWithStats(CertificationResponse):
    """Schema for certification with statistics."""
    total_completed: int = Field(default=0, description="Total employees achieved this certification")

    class Config:
        from_attributes = True

        