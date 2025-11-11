"""
Course Record Model - Database operations
Uses centralized queries from queries.py
"""
from database.connection import get_db_connection, close_db_connection
from database import queries
from typing import List, Dict, Optional
import datetime


def get_all_course_records() -> List[Dict]:
    """Get all course records"""
    connection = get_db_connection()
    if not connection:
        print("❌ Database connection failed in get_all_course_records()")
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries.GET_ALL_COURSE_RECORDS)
        records = cursor.fetchall()

        # Convert datetime to ISO strings
        for r in records:
            if isinstance(r.get("Completion_Datetime"), datetime.datetime):
                r["Completion_Datetime"] = r["Completion_Datetime"].isoformat()

        return records

    except Exception as e:
        print(f"Error in get_all_course_records: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_record_by_id(record_id: int) -> Optional[Dict]:
    """Get course record by ID"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries.GET_COURSE_RECORD_BY_ID, (record_id,))
        record = cursor.fetchone()

        if record and isinstance(record.get("Completion_Datetime"), datetime.datetime):
            record["Completion_Datetime"] = record["Completion_Datetime"].isoformat()

        return record

    except Exception as e:
        print(f"Error in get_record_by_id: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def get_records_by_employee(employee_id: str) -> List[Dict]:
    """Get all course records for an employee"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries.GET_COURSE_RECORDS_BY_EMPLOYEE, (employee_id,))
        records = cursor.fetchall()

        for r in records:
            if isinstance(r.get("Completion_Datetime"), datetime.datetime):
                r["Completion_Datetime"] = r["Completion_Datetime"].isoformat()

        return records

    except Exception as e:
        print(f"Error in get_records_by_employee: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_records_by_course(course_id: str) -> List[Dict]:
    """Get all records for a specific course"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries.GET_COURSE_RECORDS_BY_COURSE, (course_id,))
        records = cursor.fetchall()

        for r in records:
            if isinstance(r.get("Completion_Datetime"), datetime.datetime):
                r["Completion_Datetime"] = r["Completion_Datetime"].isoformat()

        return records

    except Exception as e:
        print(f"Error in get_records_by_course: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def create_record(course_id: str, employee_id: str, completion_datetime: str, document: Optional[str] = None) -> Optional[int]:
    """Create new course record"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO courses_record ( Document, Course_ID, Employee_ID) 
            VALUES ( %s, %s, %s)
        """
        cursor.execute(query, ( document, course_id, employee_id))
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error in create_record: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def update_record(record_id: int, completion_datetime: str) -> bool:
    """Update course record"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "UPDATE courses_record SET Completion_Datetime = %s WHERE Record_ID = %s"
        cursor.execute(query, (completion_datetime, record_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error in update_record: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def update_record_document(record_id: int, document: str) -> bool:
    """Update course record document"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        query = "UPDATE courses_record SET Document = %s WHERE Record_ID = %s"
        cursor.execute(query, (document, record_id))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error in update_record_document: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def delete_record(record_id: int) -> tuple:
    """Delete course record"""
    connection = get_db_connection()
    if not connection:
        return False, "Database connection failed"
    
    try:
        cursor = connection.cursor()
        
        # Get document name before deleting
        cursor.execute(queries.GET_COURSE_RECORD_DOCUMENT, (record_id,))
        result = cursor.fetchone()
        document = result[0] if result else None
        
        # Delete record
        delete_query = "DELETE FROM courses_record WHERE Record_ID = %s"
        cursor.execute(delete_query, (record_id,))
        connection.commit()

        if cursor.rowcount > 0:
            return True, document  # Return document name for file deletion
        return False, "Record not found"
        
    except Exception as e:
        print(f"Error in delete_record: {e}")
        connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
        close_db_connection(connection)


def record_exists(record_id: int) -> bool:
    """Check if course record exists"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(queries.CHECK_COURSE_RECORD_EXISTS, (record_id,))
        result = cursor.fetchone()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error in record_exists: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def get_document_path(record_id: int) -> Optional[str]:
    """Get document path for a course record"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        cursor.execute(queries.GET_COURSE_RECORD_DOCUMENT, (record_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error in get_document_path: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def employee_completed_course(employee_id: str, course_id: str) -> bool:
    """Check if employee has already completed a course"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute(queries.CHECK_EMPLOYEE_COMPLETED_COURSE, (employee_id, course_id))
        result = cursor.fetchone()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error in employee_completed_course: {e}")
        return False
    finally:
        cursor.close()
        close_db_connection(connection)