from pydantic import BaseModel, Field
from typing import Optional


class PODBase(BaseModel):
    """Base POD schema"""
    pod: str = Field(..., min_length=1, description="POD name")
    batch_code: str = Field(..., min_length=1, description="Batch code (Foreign Key)")


class PODCreate(PODBase):
    """Schema for creating a POD"""
    pod_id: str = Field(..., min_length=1, description="Unique POD ID")



class PODResponse(BaseModel):
    """Schema for POD response"""
    POD_ID: str
    POD: str
    Batch_code: str
    
    class Config:
        from_attributes = True