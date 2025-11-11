"""
Pydantic schemas for Courses API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


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


class CourseCreate(BaseModel):
    """Schema for creating new course (auto-increment ID)"""
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
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Python for QA Engineers",
                "link": "https://courses.example.com/python-qa"
            }
        }


class CourseUpdate(CourseBase):
    """Schema for updating course"""
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Advanced Python for QA",
                "link": "https://courses.example.com/python-advanced"
            }
        }


class CourseResponse(BaseModel):
    """Schema for course response"""
    Courses_ID: str
    Name: str
    Link: Optional[str]
    
    class Config:
        from_attributes = True


class CourseWithStats(CourseResponse):
    """Schema for course with statistics"""
    total_completed: int = Field(default=0, description="Total employees completed")