from models.employee import (
    get_all_employees,
    get_employee_by_id,
    get_employees_by_batch,
    create_employee,
    update_employee,
    delete_employee,
    get_employee_all_records,
    get_employee_certifications,
    get_employee_assessments,
    get_employee_courses
)

from fastapi import HTTPException
from models import employee as employee_record_db


def service_get_all_employees():
    try:
        records = get_all_employees()
        return {"success": True, "message": "Employees retrieved successfully", "data": records}
    except Exception as e:
        return {"success": False, "message": f"Error retrieving employees: {e}", "data": None}


def service_get_employee_by_id(employee_id: str):
    record = get_employee_by_id(employee_id)
    if record:
        return {"success": True, "message": "Employee retrieved successfully", "data": record}
    else:
        return {"success": False, "message": "Employee not found", "data": None}


def service_get_employees_by_batch(batch_code: int):
    try:
        records = get_employees_by_batch(batch_code)
        return {"success": True, "message": "Employees retrieved successfully", "data": records}
    except Exception as e:
        return {"success": False, "message": f"Error retrieving employees by batch: {e}", "data": None}


def service_create_employee(data):
    success = create_employee(
        data.employee_id,
        data.employee_name,
        data.employee_email,
        data.designation,
        data.batch_code
    )
    return {"success": success, "message": "Employee created successfully" if success else "Failed to create employee", "data": None}


def service_update_employee(employee_id, data):
    success = update_employee(
        employee_id,
        data.employee_name,
        data.employee_email,
        data.designation,
        data.batch_code
    )
    return {"success": success, "message": "Employee updated successfully" if success else "Failed to update employee", "data": None}


def service_delete_employee(employee_id):
    success = delete_employee(employee_id)
    return {"success": success, "message": "Employee deleted successfully" if success else "Failed to delete employee", "data": None}



def get_employee_records(employee_id: str):
    """Get all records for an employee"""
    try:
        records = employee_record_db.get_employee_all_records(employee_id)
        
        total_count = (
            len(records["certifications"]) + 
            len(records["assessments"]) + 
            len(records["courses"])
        )
        
        return {
            "success": True,
            "employee_id": employee_id,
            "data": records,
            "summary": {
                "total_certifications": len(records["certifications"]),
                "total_assessments": len(records["assessments"]),
                "total_courses": len(records["courses"]),
                "total_records": total_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employee records: {str(e)}")


def get_employee_certifications(employee_id: str):
    """Get certifications for an employee"""
    try:
        certifications = employee_record_db.get_employee_certifications(employee_id)
        
        return {
            "success": True,
            "employee_id": employee_id,
            "data": certifications,
            "total": len(certifications)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching certifications: {str(e)}")


def get_employee_assessments(employee_id: str):
    """Get assessments for an employee"""
    try:
        assessments = employee_record_db.get_employee_assessments(employee_id)
        
        return {
            "success": True,
            "employee_id": employee_id,
            "data": assessments,
            "total": len(assessments)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching assessments: {str(e)}")


def get_employee_courses(employee_id: str):
    """Get courses for an employee"""
    try:
        courses = employee_record_db.get_employee_courses(employee_id)
        
        return {
            "success": True,
            "employee_id": employee_id,
            "data": courses,
            "total": len(courses)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching courses: {str(e)}")