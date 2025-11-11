"""
Pydantic schemas for Courses API (WITH Deadline Support)
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date


class DeadlineInfo(BaseModel):
    """Deadline information for a batch"""
    batch_code: int = Field(..., gt=0)
    deadline_date: date


class CourseBase(BaseModel):
    """Base schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255, description="Course name")
    link: Optional[str] = Field(None, max_length=500, description="Course link/URL")
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Course name cannot be empty')
        return v.strip()
    
    @validator('link')
    def validate_link(cls, v):
        if v and v.strip():
            return v.strip()
        return None


class CourseCreate(CourseBase):
    """Schema for creating new course WITH deadlines"""
    courses_id: str = Field(..., min_length=1, max_length=50, description="Unique course ID")
    # deadlines: List[DeadlineInfo] = Field(..., min_items=1, description="Deadlines for different batches")
    
    @validator('courses_id')
    def courses_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Course ID cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "courses_id": "C24",
                "name": "Python for QA Engineers",
                "link": "https://courses.example.com/python-qa"
            }
        }


class CourseUpdate(CourseBase):
    """Schema for updating course (deadlines updated separately)"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Advanced Python for QA",
                "link": "https://courses.example.com/python-advanced"
            }
        }


class CourseResponse(BaseModel):
    """Schema for course response"""
    courses_id: str
    name: str
    link: Optional[str]
    
    class Config:
        from_attributes = True


class CourseWithStats(CourseResponse):
    """Schema for course with statistics"""
    total_completed: int = Field(default=0, description="Total employees completed")