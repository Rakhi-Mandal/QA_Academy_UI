from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CertificationRecordBase(BaseModel):
    """Base schema for certification record data."""
    document: Optional[str] = Field(None, max_length=255, description="Path to the certification document.")
    mark_secured: float = Field(..., ge=0, le=100, description="Mark/Score secured (0 to 100).")
    certification_id: str = Field(..., max_length=20, description="Foreign key to certification_table.")
    employee_id: str = Field(..., max_length=20, description="Foreign key to employee_table.")

class CertificationRecordCreate(CertificationRecordBase):
    """Schema for creating a new certification record."""
    pass

class CertificationRecordUpdate(CertificationRecordBase):
    """Schema for updating an existing certification record."""
    document: Optional[str] = None
    mark_secured: Optional[float] = None
    certification_id: Optional[str] = None
    employee_id: Optional[str] = None
    
    class Config:
        # Allows for partial updates
        json_schema_extra = {
            "example": {
                "document": "path/to/updated_doc.pdf",
                "mark_secured": 95.50
            }
        }

class CertificationRecordResponse(CertificationRecordBase):
    """Schema for the response body of a certification record."""
    record_id: int
    upload_time: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "record_id": 1,
                "upload_time": "2025-11-10T10:00:00",
                "document": "path/to/doc.pdf",
                "mark_secured": 88.00,
                "certification_id": "CERT001",
                "employee_id": "EMP101"
            }
        }