from database.connection import get_db_connection, close_db_connection
from typing import List, Dict, Optional
import datetime
import decimal  # ✅ to handle Decimal type conversion


def get_all_records() -> List[Dict]:
    """Get all assessment records"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Record_ID, Upload_Time, Document, Mark_Secured, Assessment_ID, Employee_ID
            FROM assessment_record
            ORDER BY Upload_Time DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()

        for r in records:
            # Convert datetime to string
            if isinstance(r.get("Upload_Time"), (datetime.datetime, datetime.date)):
                r["Upload_Time"] = r["Upload_Time"].isoformat()
            # Convert Decimal to float
            if isinstance(r.get("Mark_Secured"), decimal.Decimal):
                r["Mark_Secured"] = float(r["Mark_Secured"])

        return records

    except Exception as e:
        print(f"Error in get_all_records: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def get_record_by_id(record_id: int) -> Optional[Dict]:
    """Get specific assessment record by ID"""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Record_ID, Upload_Time, Document, Mark_Secured, Assessment_ID, Employee_ID
            FROM assessment_record
            WHERE Record_ID = %s
        """
        cursor.execute(query, (record_id,))
        record = cursor.fetchone()

        if record:
            if isinstance(record.get("Upload_Time"), (datetime.datetime, datetime.date)):
                record["Upload_Time"] = record["Upload_Time"].isoformat()
            if isinstance(record.get("Mark_Secured"), decimal.Decimal):
                record["Mark_Secured"] = float(record["Mark_Secured"])

        return record

    except Exception as e:
        print(f"Error in get_record_by_id: {e}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def get_records_by_employee(employee_id: str) -> List[Dict]:
    """Get all assessment records for a specific employee"""
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT Record_ID, Upload_Time, Document, Mark_Secured, Assessment_ID, Employee_ID
            FROM assessment_record
            WHERE Employee_ID = %s
            ORDER BY Upload_Time DESC
        """
        cursor.execute(query, (employee_id,))
        records = cursor.fetchall()

        for r in records:
            if isinstance(r.get("Upload_Time"), (datetime.datetime, datetime.date)):
                r["Upload_Time"] = r["Upload_Time"].isoformat()
            if isinstance(r.get("Mark_Secured"), decimal.Decimal):
                r["Mark_Secured"] = float(r["Mark_Secured"])

        return records

    except Exception as e:
        print(f"Error in get_records_by_employee: {e}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


def create_record(upload_time: datetime.datetime, document: str, mark_secured: float, assessment_id: str, employee_id: str) -> bool:
    """Create new assessment record"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO assessment_record (Upload_Time, Document, Mark_Secured, Assessment_ID, Employee_ID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (upload_time, document, mark_secured, assessment_id, employee_id))
        connection.commit()
        return True

    except Exception as e:
        print(f"Error in create_record: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def update_record(record_id: int, document: str, mark_secured: float) -> bool:
    """Update assessment record"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = """
            UPDATE assessment_record
            SET Document = %s, Mark_Secured = %s
            WHERE Record_ID = %s
        """
        cursor.execute(query, (document, mark_secured, record_id))
        connection.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Error in update_record: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)


def delete_record(record_id: int) -> bool:
    """Delete assessment record"""
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = "DELETE FROM assessment_record WHERE Record_ID = %s"
        cursor.execute(query, (record_id,))
        connection.commit()
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Error in delete_record: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        close_db_connection(connection)
