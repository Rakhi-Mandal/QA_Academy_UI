from models.employee import (
    get_all_employees,
    get_employee_by_id,
    get_employees_by_batch,
    create_employee,
    update_employee,
    delete_employee
)
from models.employee import (
    get_all_employees,
    get_employee_by_id,
    get_employees_by_batch,
    create_employee,
    update_employee,
    delete_employee,
    get_employee_count   # <-- add this import
)



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
        data.user_id,
        data.pod_id,
        data.employee_name,
        data.employee_id,
        data.employee_email,
        data.designation
    )
    return {"success": success, "message": "Employee created successfully" if success else "Failed to create employee", "data": None}


def service_update_employee(employee_id, data):
    success = update_employee(
        employee_id,
        data.pod_id,
        data.employee_name,
        data.employee_email,
        data.designation
    )
    return {"success": success, "message": "Employee updated successfully" if success else "Failed to update employee", "data": None}


def service_delete_employee(employee_id: str):
    success = delete_employee(employee_id)
    return {"success": success, "message": "Employee deleted successfully" if success else "Failed to delete employee", "data": None}


def service_get_employee_count():
    try:
        count = get_employee_count()
        return {"success": True, "message": "Employee count retrieved successfully", "data": {"total_employees": count}}
    except Exception as e:
        return {"success": False, "message": f"Error retrieving employee count: {e}", "data": None}
