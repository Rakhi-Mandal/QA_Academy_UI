from database.connection import get_db_connection, close_db_connection
from typing import List, Dict, Optional
from database import queries

def get_all_employees() -> List[Dict]:
    """Get all employee records with POD and Batch Code"""
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT e.user_id, e.Employee_ID, e.Employee_Name, e.Employee_Email, e.Designation,
                   e.POD_ID, p.POD, p.Batch_Code
            FROM employee_record e
            LEFT JOIN pod p ON e.POD_ID = p.POD_ID
            ORDER BY e.Employee_Name
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
    """Get specific employee record by Employee_ID"""
    connection = get_db_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT e.user_id, e.Employee_ID, e.Employee_Name, e.Employee_Email, e.Designation,
                   e.POD_ID, p.POD, p.Batch_Code
            FROM employee_record e
            LEFT JOIN pod p ON e.POD_ID = p.POD_ID
            WHERE e.Employee_ID = %s
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
    """Get employees by Batch_Code (join pod and employee_record)"""
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT e.Employee_ID, e.Employee_Name, e.Employee_Email, e.Designation,
                   e.POD_ID, p.POD, p.Batch_Code
            FROM employee_record e
            INNER JOIN pod p ON e.POD_ID = p.POD_ID
            WHERE p.Batch_Code = %s
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


def create_employee(user_id: int, pod_id: int, employee_name: str, employee_id: str, employee_email: str, designation: str) -> bool:
    """Create new employee record"""
    connection = get_db_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO employee_record (user_id, POD_ID, Employee_Name, Employee_ID, Employee_Email, Designation)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, pod_id, employee_name, employee_id, employee_email, designation))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error in create_employee: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def update_employee(employee_id: str, pod_id: int, employee_name: str, employee_email: str, designation: str) -> bool:
    """Update existing employee record by Employee_ID"""
    connection = get_db_connection()
    if not connection:
        print("❌ Database connection failed in update_employee")
        return False
    try:
        cursor = connection.cursor()
        query = """
            UPDATE employee_record
            SET POD_ID = %s,
                Employee_Name = %s,
                Employee_Email = %s,
                Designation = %s
            WHERE Employee_ID = %s
        """
        cursor.execute(query, (pod_id, employee_name, employee_email, designation, employee_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"❌ Error in update_employee: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def delete_employee(employee_id: str) -> bool:
    """Delete employee record by Employee_ID"""
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

def get_employee_count() -> int:
    """Get total count of employees"""
    connection = get_db_connection()
    if not connection:
        return 0
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) AS total_employees FROM employee_record"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error in get_employee_count: {e}")
        return 0
    finally:
        cursor.close()
        close_db_connection(connection)

def get_top_performers() -> List[Dict]:
    """Get top performers based on assessment + certification percentage"""
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries.GET_TOP_PERFORMERS)
        performers = cursor.fetchall()
        return performers
    except Exception as e:
        print(f"Error in get_top_performers: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)

