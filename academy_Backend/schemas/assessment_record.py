from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class AssessmentRecordBase(BaseModel):
    """Common fields for assessment record"""
    document: Optional[str] = Field(None, max_length=255, description="Document file path or URL")
    mark_secured: Optional[float] = Field(0.0, ge=0, le=100, description="Marks secured in assessment")
    assessment_id: str = Field(..., min_length=1, max_length=20, description="Assessment ID")
    employee_id: str = Field(..., min_length=1, max_length=20, description="Employee ID")


class AssessmentRecordCreate(AssessmentRecordBase):
    """Schema for creating assessment record"""
    upload_time: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Time of record upload")
    
    class Config:
        json_schema_extra = {
            "example": {
                "upload_time": "2025-11-10T10:30:00",
                "document": "uploads/assessments/python_test.pdf",
                "mark_secured": 88.5,
                "assessment_id": "ASM001",
                "employee_id": "EMP001"
            }
        }


class AssessmentRecordUpdate(BaseModel):
    """Schema for updating record"""
    document: Optional[str] = Field(None, max_length=255)
    mark_secured: Optional[float] = Field(None, ge=0, le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "document": "uploads/assessments/python_test_updated.pdf",
                "mark_secured": 90.0
            }
        }


class AssessmentRecordResponse(BaseModel):
    """Response schema"""
    record_id: int
    upload_time: datetime
    document: Optional[str]
    mark_secured: Optional[float]
    assessment_id: str
    employee_id: str

    class Config:
        from_attributes = True
