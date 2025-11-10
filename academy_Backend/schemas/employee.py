from pydantic import BaseModel, EmailStr
from typing import Optional


class EmployeeBase(BaseModel):
    employee_name: str
    employee_email: EmailStr
    designation: str
    batch_code: int


class EmployeeCreate(EmployeeBase):
    employee_id: str


class EmployeeUpdate(EmployeeBase):
    pass
