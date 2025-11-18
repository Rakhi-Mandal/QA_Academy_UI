from pydantic import BaseModel, Field, validator
from typing import Optional


class AssessmentBase(BaseModel):
    """Base schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255, description="Assessment name")
    link: Optional[str] = Field(None, max_length=500, description="Assessment link/URL")
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Assessment name cannot be empty')
        return v.strip()
    
    @validator('link')
    def validate_link(cls, v):
        if v and v.strip():
            return v.strip()
        return None


class AssessmentCreate(AssessmentBase):
    """Schema for creating new assessment"""
    assessment_id: str = Field(..., min_length=1, max_length=50, description="Unique assessment ID")
    
    @validator('assessment_id')
    def assessment_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Assessment ID cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "assessment_id": "ASM001",
                "name": "Python Fundamentals Test",
                "link": "https://assessment.example.com/python-test"
            }
        }


class AssessmentUpdate(AssessmentBase):
    """Schema for updating assessment"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Python Advanced Test",
                "link": "https://assessment.example.com/python-advanced"
            }
        }


class AssessmentResponse(BaseModel):
    """Schema for assessment response"""
    assessment_id: str
    name: str
    link: Optional[str]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "assessment_id": "ASM001",
                "name": "Python Fundamentals Test",
                "link": "https://assessment.example.com/python-test"
            }
        }


class AssessmentWithStats(AssessmentResponse):
    """Schema for assessment with statistics"""
    total_completed: int = Field(default=0, description="Total employees completed")
    average_score: float = Field(default=0.0, description="Average score achieved")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "assessment_id": "ASM001",
                "name": "Python Fundamentals Test",
                "link": "https://assessment.example.com/python-test",
                "total_completed": 25,
                "average_score": 87.5
            }
        }