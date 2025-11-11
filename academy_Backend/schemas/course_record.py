"""
Pydantic schemas for Course Record API
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class CourseRecordBase(BaseModel):
    """Base Course Record schema"""
    course_id: str = Field(..., min_length=1, max_length=20, description="Course ID")
    employee_id: str = Field(..., min_length=1, max_length=20, description="Employee ID")
    
    @validator('course_id', 'employee_id')
    def ids_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('ID cannot be empty')
        return v.strip()


class CourseRecordCreate(CourseRecordBase):
    """Schema for creating a new course record"""
    completion_datetime: datetime = Field(..., description="Completion date and time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "course_id": "C001",
                "employee_id": "FS452",
                "completion_datetime": "2024-11-15T14:30:00"
            }
        }


class CourseRecordUpdate(BaseModel):
    """Schema for updating a course record"""
    completion_datetime: Optional[datetime] = Field(None, description="Completion date and time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "completion_datetime": "2024-11-20T16:45:00"
            }
        }


class CourseRecordResponse(BaseModel):
    """Schema for course record response"""
    Record_ID: int
    Completion_Datetime: datetime
    Document: Optional[str]
    Course_ID: str
    Course_Name: str
    Employee_ID: str
    Employee_Name: str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "Record_ID": 1,
                "Completion_Datetime": "2024-11-15T14:30:00",
                "Document": "FS452_Course_C001.pdf",
                "Course_ID": "C001",
                "Course_Name": "Python for QA Engineers",
                "Employee_ID": "FS452",
                "Employee_Name": "Shirisha Mannem"
            }
        }