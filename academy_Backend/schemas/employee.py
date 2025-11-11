from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    pod_id: int
    employee_name: str
    employee_id: str
    employee_email: EmailStr
    designation: str


class EmployeeCreate(EmployeeBase):
    user_id: int


class EmployeeUpdate(EmployeeBase):
    pass
