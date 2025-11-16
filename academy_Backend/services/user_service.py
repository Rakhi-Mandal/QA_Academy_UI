"""
Business logic for User operations
"""
from fastapi import HTTPException
from models import user as user_db
from models import employee as employee_db

def service_get_all_users():
    try:
        records = user_db.get_all_users()
        return {"success": True, "message": "Users retrieved successfully", "data": records}
    except Exception as e:
        return {"success": False, "message": f"Error retrieving users: {e}", "data": None}


def service_get_user_by_id(user_id: int):
    record = user_db.get_user_by_id(user_id)
    if record:
        return {"success": True, "message": "User retrieved successfully", "data": record}
    else:
        return {"success": False, "message": "User not found", "data": None}


def service_create_user(data):
    """
    Create a user, and if role = 'employee',
    also create an employee record linked to this user.
    """
    try:
        # Step 1: Create the user
        success = user_db.create_user(
            data.user_mail,
            data.user_password,
            data.user_role
        )

        if not success:
            return {"success": False, "message": "❌ Failed to create user"}

        # Step 2: Fetch user_id of the newly created user
        user = user_db.get_user_by_email(data.user_mail)
        if not user:
            return {"success": False, "message": "❌ User created but not found in DB"}

        # Step 3: If role = employee, insert into employee table
        if data.user_role.lower() == "employee":
            emp_success = employee_db.create_employee(
    employee_id=data.employee_id,
    employee_name=data.employee_name,
    employee_email=data.user_mail,
    designation=data.designation,
    pod_id=data.pod_id,
    user_id=user["user_id"]   
)
       # from newly created user
            

            if not emp_success:
                return {
                    "success": True,
                    "message": "✅ User created but employee record creation failed"
                }

        return {"success": True, "message": "✅ User and Employee created successfully"}

    except Exception as e:
        return {"success": False, "message": f"Error creating user: {str(e)}"}

def service_update_user(user_id, data):
    success = user_db.update_user(user_id, data.user_password, data.user_role)
    return {"success": success, "message": "User updated successfully" if success else "Failed to update user"}


def service_delete_user(user_id):
    success = user_db.delete_user(user_id)
    return {"success": success, "message": "User deleted successfully" if success else "Failed to delete user"}

def login_user(user_mail: str, user_password: str):
    """Service for login with employee_id fetch"""

    # Step 1: Validate login from user table
    user = user_db.validate_login(user_mail, user_password)

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password",
            "data": None
        }

    user_id = user["user_id"]
    user_role = user["user_role"]

    # Step 2: Default employee_id
    employee_id = None

    # Step 3: If user is employee → get employee_id from employee table
    if user_role.lower() == "employee":
        employee = employee_db.get_employee_by_user_id(user_id)
        if employee:
            employee_id = employee["Employee_ID"]  # from employee table

    # Step 4: Return user info + employee_id
    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "user_id": user_id,
            "user_mail": user_mail,
            "user_role": user_role,
            "employee_id": employee_id
        }
    }
