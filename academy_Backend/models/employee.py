from database.connection import get_db_connection, close_db_connection
from typing import List, Dict, Optional


def get_all_employees() -> List[Dict]:
    """Get all employee records"""
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Employee_ID, Employee_Name, Employee_Email, Designation, Batch_Code
            FROM employee_record
            ORDER BY Employee_Name
        """
        cursor.execute(query)
        employees = cursor.fetchall()
        return employees
    except Exception as e:
        print(f"Error in get_all_employees: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_employee_by_id(employee_id: str) -> Optional[Dict]:
    """Get specific employee record"""
    connection = get_db_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Employee_ID, Employee_Name, Employee_Email, Designation, Batch_Code
            FROM employee_record
            WHERE Employee_ID = %s
        """
        cursor.execute(query, (employee_id,))
        employee = cursor.fetchone()
        return employee
    except Exception as e:
        print(f"Error in get_employee_by_id: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def get_employees_by_batch(batch_code: int) -> List[Dict]:
    """Get employees by batch code"""
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Employee_ID, Employee_Name, Employee_Email, Designation, Batch_Code
            FROM employee_record
            WHERE Batch_Code = %s
        """
        cursor.execute(query, (batch_code,))
        employees = cursor.fetchall()
        return employees
    except Exception as e:
        print(f"Error in get_employees_by_batch: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def create_employee(employee_id: str, employee_name: str, employee_email: str, designation: str, batch_code: int) -> bool:
    """Create new employee record"""
    connection = get_db_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO employee_record (Employee_ID, Employee_Name, Employee_Email, Designation, Batch_Code)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (employee_id, employee_name, employee_email, designation, batch_code))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error in create_employee: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def update_employee(employee_id, employee_name, employee_email, designation, batch_code):
    """Update an existing employee record"""
    connection = get_db_connection()
    if not connection:
        print("❌ Database connection failed in update_employee")
        return False

    try:
        cursor = connection.cursor()
        query = """
            UPDATE employee_record
            SET Employee_Name = %s,
                Employee_Email = %s,
                Designation = %s,
                Batch_Code = %s
            WHERE Employee_ID = %s
        """
        print("🧠 Query:", query)
        print("🧠 Values:", (employee_name, employee_email, designation, batch_code, employee_id))

        cursor.execute(query, (employee_name, employee_email, designation, batch_code, employee_id))
        connection.commit()

        print("✅ Rows affected:", cursor.rowcount)
        return cursor.rowcount > 0
    except Exception as e:
        print("❌ Error in update_employee:", e)
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def delete_employee(employee_id: str) -> bool:
    """Delete employee record"""
    connection = get_db_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        query = "DELETE FROM employee_record WHERE Employee_ID = %s"
        cursor.execute(query, (employee_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error in delete_employee: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)
