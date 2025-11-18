from fastapi import APIRouter,Path
from schemas.employee import EmployeeCreate, EmployeeUpdate
from services.employee_service import (
    service_get_all_employees,
    service_get_employee_by_id,
    service_get_employee_count,
    service_get_employees_by_batch,
    service_create_employee,
    service_update_employee,
    service_delete_employee,
    service_get_top_performers
)

# import the employee_service module as an alias so route functions call module functions
import services.employee_service as employee_record_service

# ✅ No prefix or tags here — they are handled in main.py
router = APIRouter()
@router.get("/count")
def get_employee_count():
    """Get total number of employees"""
    return service_get_employee_count()

@router.get("/")
def get_all_employees():
    """Get all employee records"""
    return service_get_all_employees()

@router.get("/top-performers")
def get_top_performers():
    """Get top performers based on assessments + certifications percentage"""
    return service_get_top_performers()

@router.get("/{employee_id}")
def get_employee_by_id(employee_id: str):
    """Get specific employee record"""
    return service_get_employee_by_id(employee_id)


@router.get("/batch/{batch_code}")
def get_employees_by_batch(batch_code: int):
    """Get employees by batch code"""
    return service_get_employees_by_batch(batch_code)


@router.post("/")
def create_employee(data: EmployeeCreate):
    """Create new employee"""
    return service_create_employee(data)


@router.put("/{employee_id}")
def update_employee(employee_id: str, data: EmployeeUpdate):
    """Update existing employee record"""
    return service_update_employee(employee_id, data)


@router.delete("/{employee_id}")
def delete_employee(employee_id: str):
    """Delete employee record"""
    return service_delete_employee(employee_id)


@router.get("/{employee_id}/all")
def get_employee_all_records(
    employee_id: str = Path(..., description="Employee ID")
):
    """
    Get all records (certifications, assessments, courses) for an employee
    
    Returns separate arrays for each type without null values
    """
    return employee_record_service.get_employee_records(employee_id)


@router.get("/{employee_id}/certifications")
def get_employee_certifications(
    employee_id: str = Path(..., description="Employee ID")
):
    """Get all certifications for an employee"""
    return employee_record_service.get_employee_certifications(employee_id)


@router.get("/{employee_id}/assessments")
def get_employee_assessments(
    employee_id: str = Path(..., description="Employee ID")
):
    """Get all assessments for an employee"""
    return employee_record_service.get_employee_assessments(employee_id)


@router.get("/{employee_id}/courses")
def get_employee_courses(
    employee_id: str = Path(..., description="Employee ID")
):
    """Get all courses for an employee"""
    return employee_record_service.get_employee_courses(employee_id)