from database.connection import get_db_connection, close_db_connection
from typing import List, Dict, Optional, Tuple


def get_all_pods() -> List[Dict]:
    """Get all PODs from database"""
    connection = get_db_connection()
    if not connection:
        print("Database connection failed in get_all_pods()")
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT POD_ID, POD, Batch_code
            FROM pod
        """
        print("📄 Executing query:", query)
        cursor.execute(query)
        pods = cursor.fetchall()

        print(f"🔍 Total rows fetched: {len(pods)}")
        return pods

    except Exception as e:
        print(f"Error in get_all_pods: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_pod_by_id(pod_id: str) -> Optional[Dict]:
    """Get specific POD by ID"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT POD_ID, POD, Batch_code
            FROM pod
            WHERE POD_ID = %s
        """
        cursor.execute(query, (pod_id,))
        pod = cursor.fetchone()
        return pod

    except Exception as e:
        print(f"Error in get_pod_by_id: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def get_pods_by_batch(batch_code: str) -> List[Dict]:
    """Get all PODs for a specific batch"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT POD_ID, POD, Batch_code
            FROM pod
            WHERE Batch_code = %s
            ORDER BY POD_ID
        """
        cursor.execute(query, (batch_code,))
        pods = cursor.fetchall()
        return pods

    except Exception as e:
        print(f"Error in get_pods_by_batch: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def create_pod(pod_id: str, pod_name: str, batch_code: str) -> Tuple[bool, str]:
    """Create new POD"""
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()
        
        # Check if batch_code exists
        check_batch_query = "SELECT COUNT(*) FROM batch_table WHERE Batch_Code = %s"
        cursor.execute(check_batch_query, (batch_code,))
        result = cursor.fetchone()
        
        if not result or result[0] == 0:
            return False, f"Batch '{batch_code}' does not exist"
        
        # Insert POD
        query = """
            INSERT INTO pod (POD_ID, POD, Batch_code)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (pod_id, pod_name, batch_code))
        connection.commit()
        return True, "POD created successfully"
        
    except Exception as e:
        print(f"Error in create_pod: {e}")
        connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
        close_db_connection(connection)


def pod_exists(pod_id: str) -> bool:
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM pod WHERE POD_ID = %s"
        cursor.execute(query, (pod_id,))
        result = cursor.fetchone()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error in pod_exists: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def batch_exists(batch_code: str) -> bool:
    """Check if batch exists"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM batch_table WHERE Batch_Code = %s"
        cursor.execute(query, (batch_code,))
        result = cursor.fetchone()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error in batch_exists: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def get_employees_by_pod(pod_id: str):
    """Fetch all employees under a specific POD"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT 
                Employee_ID,
                Employee_Name,
                Employee_Email,
                Designation,
                POD_ID
            FROM employee_record
            WHERE POD_ID = %s
        """
        cursor.execute(query, (pod_id,))
        employees = cursor.fetchall()
        return employees
    except Exception as e:
        print(f"Error in get_employees_by_pod: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)