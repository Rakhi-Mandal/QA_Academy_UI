from fastapi import APIRouter
from schemas.employee import EmployeeCreate, EmployeeUpdate
from services.employee_service import (
    service_get_all_employees,
    service_get_employee_by_id,
    service_get_employee_count,
    service_get_employees_by_batch,
    service_create_employee,
    service_update_employee,
    service_delete_employee
)

router = APIRouter()

@router.get("/count")
def get_employee_count():
    """Get total number of employees"""
    return service_get_employee_count()

@router.get("/")
def get_all_employees():
    """Get all employee records"""
    return service_get_all_employees()


@router.get("/{employee_id}")
def get_employee_by_id(employee_id: str):
    """Get specific employee record by Employee_ID"""
    return service_get_employee_by_id(employee_id)


@router.get("/batch/{batch_code}")
def get_employees_by_batch(batch_code: int):
    """Get employees by batch code"""
    return service_get_employees_by_batch(batch_code)


@router.post("/add")
def create_employee(data: EmployeeCreate):
    """Create new employee"""
    return service_create_employee(data)


@router.put("/{employee_id}")
def update_employee(employee_id: str, data: EmployeeUpdate):
    """Update existing employee record by Employee_ID"""
    return service_update_employee(employee_id, data)


@router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    """Delete employee record by Employee_ID"""
    return service_delete_employee(employee_id)


