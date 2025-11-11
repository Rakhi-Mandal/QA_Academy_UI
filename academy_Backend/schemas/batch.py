from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class BatchBase(BaseModel):
    """Base batch schema"""
    batch_name: str = Field(..., min_length=1, description="Batch name")